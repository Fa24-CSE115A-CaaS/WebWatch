import difflib
from sqlmodel import Session, select
from schemas.user import User
import os


def compare_texts(text1, text2):
    diff = difflib.unified_diff(
        text1.splitlines(),
        text2.splitlines(),
        lineterm="",
        fromfile="first_scrape",
        tofile="second_scrape",
    )
    return "\n".join(diff)


def get_user_from_id(user_id: int):
    from database import Database

    db = Database(mode=os.getenv("ENV"))
    with next(db.get_session()) as session:
        result = session.exec(select(User).where(User.id == user_id)).first()
    return result


def update_content_in_db(task_id: int, new_content: str):
    from database import Database
    from schemas.task import Task

    db = Database(mode=os.getenv("ENV"))
    with next(db.get_session()) as session:
        task = session.exec(select(Task).where(Task.id == task_id)).first()
        if task:
            task.content = new_content
            session.add(task)
            session.commit()
            session.refresh(task)
