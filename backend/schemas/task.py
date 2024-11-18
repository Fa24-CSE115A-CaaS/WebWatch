from sqlalchemy import Column
from typing import List, Literal
from sqlalchemy.types import JSON, String
from pydantic import field_validator
from sqlmodel import SQLModel, Field, select
import logging
import asyncio
from schemas.user import User
import os
from utils.scan_helpers import compare_texts, get_user_from_id, update_content_in_db

NotificationOptions = List[Literal["EMAIL", "DISCORD", "SLACK"]]

# Configure logging
logging.basicConfig(level=logging.INFO)
logging.getLogger("sqlalchemy.engine").setLevel(
    logging.WARNING
)  # Adjust SQLAlchemy log level to reduce noise


class TaskBase(SQLModel):
    name: str = Field(max_length=50)
    content: str | None = Field(default=None, sa_column=Column(String(length=10000)))
    url: str
    discord_url: str | None = None
    enabled_notification_options: NotificationOptions = Field(
        default=["EMAIL"], sa_column=Column(JSON())
    )
    enabled: bool = True  # If the task is enabled then it should be running

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
            await asyncio.sleep(30)


class Task(TaskBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")

    def get_id(self):
        # Returns the task_id
        return self.id

    def scan(self):
        from scrape import WebScraper
        from utils.notifications import send_mail

        try:
            with WebScraper() as scraper:
                new_content = scraper.scrape_all_text(self.url)
        except Exception as e:
            logging.error(f"An error occurred while scraping {self.name}: {e}")
            """
            send_mail(
                f"Error scraping {self.name}",
                f"An error occurred while scraping {self.name}.",
                [get_user_from_id(self.user_id).email],
            )
            """
            return

        if new_content is None:
            logging.error(f"An error occurred while scraping {self.name}.")
            """
            send_mail(
                f"Error scraping {self.name}",
                f"An error occurred while scraping {self.name}.",
                [get_user_from_id(self.user_id).email],
            )
            """
            return

        # If stored content is None (such as on the first scan), store the new content
        if self.content is None:
            logging.info(f"Initial scan for task id: {self.id}. Writing to database.")
            try:
                update_content_in_db(self.id, new_content)
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
                update_content_in_db(self.id, new_content)
                self.content = new_content
                subject = "WebWatch Change Report"
                """
                send_mail(
                    subject,
                    f"Changes have been detected on {self.url}.\n\n {diff}",
                    [
                        get_user_from_id(self.user_id).email
                    ],  # Send email to user's address
                )
                """
            except Exception as e:
                logging.error(f"Failed to update content in DB or send email: {e}")
        else:
            logging.info(f"No change detected for task id: {self.id}.")


class TaskGet(TaskBase):
    id: int
    user_id: int


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    name: str | None = Field(default=None, max_length=50)
    content: str | None = Field(default=None, sa_column=Column(String(length=10000)))
    url: str | None = None
    discord_url: str | None = None
    enabled_notification_options: NotificationOptions | None = Field(
        default=None, sa_column=Column(JSON())
    )
    enabled: bool | None = None
