from sqlmodel import SQLModel, Session, create_engine, select
from schemas.task import TaskCreate, Task
import os


class Database:
    def __init__(self, mode: str = "DEV"):
        self.engine = None

        if mode == "PRODUCTION":
            self._create_mysql()
        else:
            self._create_sqlite()

        SQLModel.metadata.create_all(self.engine)

    def _create_sqlite(self):
        db_filename = "database.db"
        db_url = f"sqlite:///{db_filename}"
        self.engine = create_engine(db_url, echo=True)

    def _create_mysql(self):
        username = os.getenv("MYSQL_USERNAME")
        password = os.getenv("MYSQL_PASSWORD")
        server = os.getenv("MYSQL_SERVER")
        dbname = os.getenv("MYSQL_DBNAME")
        db_url = (
            f"mysql+pymysql://{username}:{password}@{server}/{dbname}?charset=utf8mb4"
        )
        self.engine = create_engine(db_url, echo=False, pool_recycle=3600)

    def get_session(self):
        with Session(self.engine) as session:
            yield session


# DEMO
if __name__ == "__main__":
    db = Database(mode=os.getenv("ENV"))
    session = next(db.get_session())

    # INSERTION DEMO
    input = TaskCreate(
        name="DEMO TASK",
        content="FILLER",
        url="FILLER",
        enabled_notification_options=["EMAIL"],
    )
    new_task = Task.model_validate(input)
    session.add(new_task)
    session.commit()

    # SELECTION DEMO
    statement = select(Task).where(Task.name.in_(["DEMO TASK"]))
    for task in session.exec(statement):
        print(f"Name: {task.name}\tContent: {task.content}")
