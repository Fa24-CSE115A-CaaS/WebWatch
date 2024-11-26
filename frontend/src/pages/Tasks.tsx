import { useEffect, useState } from "react";
// Components
import TaskList from "../components/TaskList";
import CreateInput from "../components/CreateInput";
// Hooks
import useAuth from "../hooks/useAuth";
// Types
import { Task, TaskResponse } from "../types";

const Tasks = () => {
  const { user, isTokenValid } = useAuth({ redirectToAuth: true });
  const [tasks, setTasks] = useState<Task[]>([]);

  useEffect(() => {
    if (!isTokenValid) return;

    let valid = true;
    const token = localStorage.getItem("access_token");
    const baseUrl = import.meta.env.VITE_ROOT_API;
    const socket = new WebSocket(`${baseUrl}/tasks/ws?token=${token}`);

    socket.addEventListener("message", (e) => {
      if (!valid) {
        return;
      }

      const taskResponse = JSON.parse(e.data);
      const now = new Date();
      const offset = -now.getTimezoneOffset();

      const tasks: Task[] = taskResponse.map((data: TaskResponse) => {
        const nextRunMs = Date.parse(data.next_run);
        const nextRun = new Date(nextRunMs + offset * 60_000);

        return {
          id: data.id,
          name: data.name,
          content: data.content,
          url: data.url,
          discordUrl: data.discord_url,
          interval: data.interval,
          enabledNotificationOptions: data.enabled_notification_options,
          enabled: data.enabled,
          nextRun,
        } as Task;
      });
      setTasks(tasks);
    });

    return () => {
      valid = false;
      socket.close();
    };
  }, [isTokenValid]);

  if (!isTokenValid) {
    return <div>Loading...</div>;
  }

  return (
    <main className="text-text">
      <CreateInput />
      <div className="mx-3 sm:mx-8 xl:mx-auto xl:w-[1200px] xxl:w-[1500px]">
        <h1 className="mb-5 text-2xl font-semibold">Running</h1>
        <TaskList tasks={tasks.filter((t) => t.enabled)} />
      </div>
      <div className="mx-3 sm:mx-8 xl:mx-auto xl:w-[1200px] xxl:w-[1500px]">
        <h1 className="mb-5 text-2xl font-semibold">Paused</h1>
        <TaskList tasks={tasks.filter((t) => !t.enabled)} />
      </div>
      {user && <p className="mt-4 text-center">Logged in as: {user.email}</p>}
    </main>
  );
};

export default Tasks;
