// Components
import TaskList from "../components/TaskList";
import CreateInput from "../components/CreateInput";
import { useEffect, useState } from "react";
import { Task, TaskResponse } from "../types";
import { axios } from "../config";

const Tasks = () => {
  const [runningTasks, setRunningTasks] = useState<Task[]>([]);
  const [pausedTasks, setPausedTasks] = useState<Task[]>([]);

  useEffect(() => {
    let valid = true;
    const fetchTasks = async () => {
      const token = localStorage.getItem("token");
      const response = await axios.get("/tasks", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (response.status === 200 && valid) {
        const tasks: Task[] = response.data.map((data: TaskResponse) => {
          return {
            id: data.id,
            name: data.name,
            content: data.content,
            url: data.url,
            discordUrl: data.discord_url,
            enabledNotificationOptions: data.enabled_notification_options,
            enabled: data.enabled,
          } as Task;
        });

        setRunningTasks(tasks.filter((t) => t.enabled));
        setPausedTasks(tasks.filter((t) => !t.enabled));
      }
    };
    fetchTasks();
    return () => {
      valid = false;
    };
  }, []);

  return (
    <main className="text-text">
      <CreateInput />
      <div className="mx-auto xl:w-[1200px] xxl:w-[1500px]">
        <h1 className="mb-5 text-2xl font-semibold">Running</h1>
        <TaskList tasks={runningTasks} />
      </div>
      <div className="mx-auto xl:w-[1200px] xxl:w-[1500px]">
        <h1 className="mb-5 text-2xl font-semibold">Paused</h1>
        <TaskList tasks={pausedTasks} />
      </div>
    </main>
  );
};

export default Tasks;
