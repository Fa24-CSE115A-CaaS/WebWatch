import asyncio
import logging
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


class task_obj:
    def __init__(self, task_id: int, content: str):
        self.task_id = task_id
        self.content = content  # CONTENT FORMATTING IS SUBJECTIVE TO CHANGE

    def get_id(self):
        # Returns the task_id
        return self.task_id

    def proc_init(self):
        # Initializes the async function in the new process
        return asyncio.run(self.run())

    async def run(self):
        # PLACEHOLDER
        await asyncio.sleep(1)
        print(self.task_id)


class scheduler_obj:
    def __init__(self):
        self.executor = ProcessPoolExecutor()
        self.loop = asyncio.new_event_loop()
        self.running_tasks = dict()

    async def add_task(self, task: task_obj):
        # Spawns task in a new process
        if self.running_tasks.get(task.get_id()):
            logging.warning(f"{task.get_id()} is already running")
        else:
            self.running_tasks[task.get_id()] = self.loop.run_in_executor(
                self.executor, task.proc_init
            )
            logging.info(f"{task.get_id()} is now running")

    async def remove_task(self, task: task_obj):
        # Kills task based on id passed
        async_task = self.running_tasks.get(task.get_id())
        if async_task:
            task.cancel()
            logging.info(f"{task.get_id()} is now stopped")
        else:
            logging.warning(f"{task.get_id()} is already stopped")

    async def restart_task(self, task: task_obj):
        # Mapping to stopping then starting
        self.remove_task(task)
        self.add_task(task)


# # TESTING CODE
# async def main():
#     scheduler = scheduler_obj()
#     res = [scheduler.add_task(task_obj(i, "FILLER")) for i in range(0, 128)]

#     await asyncio.gather(*res)


# if __name__ == "__main__":
#     asyncio.run(main())
