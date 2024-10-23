import asyncio
import logging
from schemas.task import Task, TaskCreate, TaskGet, TaskUpdate
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


class Scheduler:
    def __init__(self):
        self.executor = ProcessPoolExecutor()
        self.loop = asyncio.new_event_loop()
        self.running_tasks = dict()

    async def shutdown(self):
        for _, task in self.running_tasks:
            task.cancel()

    async def status(self, task: Task) -> str:
        if task.get_id() in self.running_tasks:
            return f"{task.get_id()} is running"
        else:
            return f"{task.get_id()} is not running"

    async def add_task(self, task: Task):
        # Spawns task in a new process
        if self.running_tasks.get(task.get_id()):
            logging.warning(f"{task.get_id()} is already running")
        else:
            self.running_tasks[task.get_id()] = self.loop.run_in_executor(
                self.executor, task.proc_init
            )
            logging.info(f"{task.get_id()} is now running")

    async def remove_task(self, task: Task):
        # Kills task based on id passed
        async_task = self.running_tasks.get(task.get_id())
        if async_task:
            async_task.cancel()
            logging.info(f"{task.get_id()} is now stopped")
        else:
            logging.warning(f"{task.get_id()} is already stopped")

    async def restart_task(self, task: Task):
        # Mapping to stopping then starting
        self.remove_task(task)
        self.add_task(task)


# # TESTING CODE
# async def main():
#     scheduler = Scheduler()
#     res = [scheduler.add_task(task_obj(i, "FILLER")) for i in range(0, 128)]

#     await asyncio.gather(*res)


# if __name__ == "__main__":
#     asyncio.run(main())
