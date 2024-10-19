import sqlalchemy
import sqlalchemy.orm
import os


class Base(sqlalchemy.orm.DeclarativeBase):
    pass


class Tasks(
    Base
):  # EXAMPLE WITH TASKS <-- Build something similiar to this for the other datatypes
    __tablename__ = "Tasks"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, unique=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    content = sqlalchemy.Column(sqlalchemy.String)


class Database:
    def __init__(
        self, production: bool = False
    ):  # By default it will make something in the SQLITE memory database, set production to True to use MYSQL
        self.engine = None
        if production:
            self._create_mysql()
        else:
            self._create_sqlite()

        # Initialize your tables here
        Tasks.metadata.create_all(self.engine)

    def _create_sqlite(self):
        self.engine = sqlalchemy.create_engine(
            "sqlite://", echo=True
        )  # THIS CREATE A SQLITE ENGINE IN MEMORY

    def _create_mysql(self):
        username = os.getenv("MYSQL_USERNAME")
        password = os.getenv("MYSQL_PASSWORD")
        server = os.getenv("MYSQL_SERVER")
        self.engine = sqlalchemy.create_engine(
            f"mysql+pymysql://{username}:{password}@{server}/dbname?charset=utf8mb4",
            echo=False,
            pool_recycle=3600,
        )  # THIS CREATES A MYSQL/MARIADB ENGINE

    def get_engine(self):
        return self.engine


# DEMO
if __name__ == "__main__":
    db = Database()

    # INSERTION DEMO
    with sqlalchemy.orm.Session(db.get_engine()) as session:
        session.add_all([Tasks(name="DEMO TASK", content="FILLER")])
        session.commit()

    # SELECTION DEMO

    with sqlalchemy.orm.Session(db.get_engine()) as session:
        statement = sqlalchemy.select(Tasks).where(Tasks.name.in_(["DEMO TASK"]))
        for task in session.scalars(statement):
            print(f"Name: {task.name}\tContent: {task.content}")
