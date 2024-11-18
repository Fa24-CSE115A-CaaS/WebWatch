import TaskList from "../components/TaskList";
import CreateInput from "../components/CreateInput";
import {
  createContext,
  Dispatch,
  SetStateAction,
  useEffect,
  useState,
} from "react";
import { Task, TaskResponse } from "../types";
import { axios } from "../config";
import useAuth from "../hooks/useAuth";

interface TaskPageContext {
  tasks: Task[];
  setTasks: Dispatch<SetStateAction<Task[]>>;
}

export const TasksPageContext = createContext<TaskPageContext | null>(null);

const Tasks = () => {
  const { user, isTokenValid } = useAuth({ redirectToAuth: true });
  const [tasks, setTasks] = useState<Task[]>([]);

  useEffect(() => {
    if (!isTokenValid) return;

    let valid = true;
    const fetchTasks = async () => {
      const response = await axios.get("/tasks", {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("access_token")}`,
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
            interval: data.interval,
            enabledNotificationOptions: data.enabled_notification_options,
            enabled: data.enabled,
          } as Task;
        });
        setTasks(tasks);
      }
    };
    fetchTasks();
    return () => {
      valid = false;
    };
  }, [isTokenValid]);

  if (!isTokenValid) {
    return <div>Loading...</div>;
  }

  return (
    <TasksPageContext.Provider value={{ tasks, setTasks }}>
      <main className="text-text">
        <CreateInput />
        <div className="mx-auto xl:w-[1200px] xxl:w-[1500px]">
          <h1 className="mb-5 text-2xl font-semibold">Running</h1>
          <TaskList tasks={tasks.filter((t) => t.enabled)} />
        </div>
        <div className="mx-auto xl:w-[1200px] xxl:w-[1500px]">
          <h1 className="mb-5 text-2xl font-semibold">Paused</h1>
          <TaskList tasks={tasks.filter((t) => !t.enabled)} />
        </div>
        {user && <p className="mt-4 text-center">Logged in as: {user.email}</p>}
      </main>
    </TasksPageContext.Provider>
  );
};

export default Tasks;
