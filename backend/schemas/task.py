from sqlalchemy import Column, types
from typing import List, Literal
from sqlalchemy.types import JSON, String, DateTime
from pydantic import field_validator, HttpUrl, validator, ValidationError
from sqlmodel import SQLModel, Field
import logging
import asyncio
from task_websocket_manager import get_task_manager
from utils.scan_helpers import compare_texts, get_user_from_id, update_task_field
from constants.task import MIN_INTERVAL_SECONDS, MAX_INTERVAL_SECONDS
from datetime import datetime, timezone, timedelta

NotificationOptions = List[Literal["EMAIL", "DISCORD", "SLACK"]]

# Configure logging
logging.basicConfig(level=logging.INFO)
logging.getLogger("sqlalchemy.engine").setLevel(
    logging.WARNING
)  # Adjust SQLAlchemy log level to reduce noise

manager = get_task_manager()


class URLType(types.TypeDecorator):
    impl = types.String

    def process_bind_param(self, value, dialect):
        if value:
            try:
                # Validate URL format by creating an instance of HttpUrl
                HttpUrl(value)
            except ValidationError as e:
                raise ValueError(f"Invalid URL: {e}")
            return str(value)
        return None

    def process_result_value(self, value, dialect):
        return value


class TaskBase(SQLModel):
    name: str = Field(max_length=50)
    url: str = Field(sa_column=Column(URLType))
    discord_url: str | None = Field(sa_column=Column(URLType), default=None)
    slack_url: str | None = Field(sa_column=Column(URLType), default=None)
    interval: int = Field(ge=MIN_INTERVAL_SECONDS, le=MAX_INTERVAL_SECONDS)
    enabled_notification_options: NotificationOptions = Field(
        default=["EMAIL"], sa_column=Column(JSON())
    )
    enabled: bool = True  # If the task is enabled then it should be running

    @validator("url", "discord_url", "slack_url")
    def validate_url(cls, value):
        if value is None:
            return value
        if not value:
            raise ValueError("URL cannot be empty")
        try:
            HttpUrl(value)
        except ValidationError as e:
            raise ValueError(f"Invalid URL: {e}")
        return value

    @field_validator("enabled_notification_options")
    @classmethod
    def notification_choice_validator(cls, value: NotificationOptions):
        unique = set()
        for option in value:
            if option in unique:
                raise ValueError(f"duplicate notification option not allowed {option}")
            unique.add(option)
        return value

    def proc_init(self):
        # Initializes the async function in the new process
        return asyncio.run(self.run())

    async def run(self):
        # TODO: Implement scanning logic

        loop = asyncio.get_event_loop()
        try:
            user = await loop.run_in_executor(None, get_user_from_id, self.user_id)
        except Exception as e:
            logging.error(f"Failed to get user: {e}")
            return

        while self.enabled:
            logging.info(f"User {user.email}: scan {self.url}")
            try:
                await loop.run_in_executor(None, self.scan)
            except Exception as e:
                logging.error(f"Error during scan: {e}")
            await asyncio.sleep(self.interval)


class Task(TaskBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    content: str | None = Field(default=None, sa_column=Column(String(length=10000)))
    next_run: datetime | None = Field(
        sa_column=Column(DateTime(), nullable=True, default=None)
    )

    def get_id(self):
        # Returns the task_id
        return self.id

    def notify(self, message: dict):
        from utils.notifications import send_mail, send_discord_msg, send_slack_msg

        subject = message["subject"]
        body = message["body"]

        # Notify the user based on the enabled notification options
        if "EMAIL" in self.enabled_notification_options:
            """
            try:
                send_mail(
                    subject,
                    body,
                    [get_user_from_id(self.user_id).email],
                )
            except Exception as e:
                logging.error(f"Failed to send email: {e}")
            """
            pass

        if "DISCORD" in self.enabled_notification_options:
            # send discord message
            try:
                send_discord_msg(self.discord_url, body)
            except Exception as e:
                logging.error(f"Failed to send discord message: {e}")
            pass
        if "SLACK" in self.enabled_notification_options:
            # send slack message
            try:
                send_slack_msg(self.slack_url, body)
            except Exception as e:
                logging.error(f"Failed to send slack message: {e}")
            pass

    def scan(self):
        from scrape import WebScraper

        error_message = {
            "subject": f"An error occurred while scraping {self.url}",
            "body": f"An error occurred while scraping {self.url}. Please modify your task to include a valid URL.",
        }
        update_task_field(
            self.id,
            "next_run",
            datetime.now(timezone.utc) + timedelta(seconds=self.interval),
        )
        manager.notify_conections(self.user_id)
        try:
            with WebScraper() as scraper:
                new_content = scraper.scrape_all_text(self.url)
        except Exception as e:
            logging.error(
                f"Task {self.id} encountered an error while scraping {self.url}: {e}"
            )
            self.notify(error_message)
            return

        if new_content is None:
            logging.error(f"An error occurred while scraping {self.name}.")
            self.notify(error_message)
            return

        # If stored content is None (such as on the first scan), store the new content
        if self.content is None:
            logging.info(f"Initial scan for task id: {self.id}. Writing to database.")
            try:
                update_task_field(self.id, "content", new_content)
                self.content = new_content
            except Exception as e:
                logging.error(f"Failed to update content in DB: {e}")
            return

        # Compare the new content with the old content
        try:
            diff = compare_texts(self.content, new_content)
        except Exception as e:
            logging.error(f"Failed to compare texts: {e}")
            return

        if diff:
            logging.info(
                f"Change detected for task id: {self.id}. Writing to database and sending email."
            )
            try:
                update_task_field(self.id, "content", new_content)
                self.content = new_content
            except Exception as e:
                logging.error(f"Failed to update content in DB: {e}")

            message = {
                "subject": "WebWatch Change Report",
                "body": f"Changes have been detected on {self.url}.\n\n {diff}",
            }
            self.notify(message)
        else:
            logging.info(f"No change detected for task id: {self.id}.")


class TaskGet(TaskBase):
    id: int
    user_id: int
    next_run: datetime | None = Field(
        sa_column=Column(DateTime(), nullable=True, default=None)
    )


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    name: str | None = Field(default=None, max_length=50)
    url: str | None = None
    discord_url: str | None = None
    slack_url: str | None = None
    interval: int | None = Field(
        default=None, ge=MIN_INTERVAL_SECONDS, le=MAX_INTERVAL_SECONDS
    )
    enabled_notification_options: NotificationOptions | None = Field(
        default=None, sa_column=Column(JSON())
    )
    enabled: bool | None = None

    @validator("url", "discord_url", "slack_url", pre=True, always=True)
    def validate_url(cls, value):
        if value is None or value == "":
            return value
        if not value:
            raise ValueError("URL cannot be empty")
        try:
            HttpUrl(value)
        except ValidationError as e:
            raise ValueError(f"Invalid URL: {e}")
        return value
