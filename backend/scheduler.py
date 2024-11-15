import asyncio
import logging
from schemas.task import Task, TaskCreate, TaskGet, TaskUpdate
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


class Scheduler:
    _instance = None

    # Singleton pattern to ensure only one instance of the scheduler is created
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Scheduler, cls).__new__(cls)
            cls._instance.__init__()
        return cls._instance

    def __init__(self):
        if not hasattr(self, "executor"):
            self.executor = ProcessPoolExecutor()
            self.loop = asyncio.new_event_loop()
            self.running_tasks = dict()

    async def shutdown(self):
        for task in self.running_tasks.values():
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass

    async def status(self, task: Task) -> str:
        if task.get_id() in self.running_tasks:
            return f"{task.get_id()} is running"
        else:
            return f"{task.get_id()} is not running"

    async def add_task(self, task: Task):
        # Spawns task in a new process
        if self.running_tasks.get(task.get_id()):
            logging.warning(f"Task {task.get_id()} is already running")
        else:
            logging.info(f"Creating async task for {task.get_id()}")
            async_task = asyncio.create_task(task.run())
            self.running_tasks[task.get_id()] = async_task
            logging.info(f"Task {task.get_id()} is now running and added to running_tasks")

    async def remove_task(self, task: Task):
        # Kills task based on id passed
        async_task = self.running_tasks.get(task.get_id())
        if async_task:
            logging.info(f"Attempting to cancel task {task.get_id()}")
            async_task.cancel()
            try:
                await async_task
            except asyncio.CancelledError:
                logging.info(f"Task {task.get_id()} has been cancelled")
            del self.running_tasks[task.get_id()]
            logging.info(f"Task {task.get_id()} removed from running_tasks")
        else:
            logging.warning(f"Task {task.get_id()} is already stopped or not found in running_tasks")

    async def restart_task(self, task: Task):
        # Mapping to stopping then starting
        await self.remove_task(task)
        await self.add_task(task)

scheduler_instance = Scheduler()
def get_scheduler():
    return scheduler_instance

# # TESTING CODE
# async def main():
#     scheduler = Scheduler()
#     res = [scheduler.add_task(task_obj(i, "FILLER")) for i in range(0, 128)]

#     await asyncio.gather(*res)


# if __name__ == "__main__":
#     asyncio.run(main())
