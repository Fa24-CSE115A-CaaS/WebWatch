import { useContext } from "react";
// Icons
import { HiDotsVertical } from "react-icons/hi";
// Hooks
import usePopup from "../../hooks/usePopup";
// Context
import { TasksPageContext } from "../../pages/Tasks";
// Types
import { TaskComponent } from "./types";
// Util
import { axios } from "../../config";

const Task: TaskComponent = ({ task, onEditModalOpen }) => {
  const { tasks, setTasks } = useContext(TasksPageContext)!;
  const { open, setOpen, containerRef } = usePopup();

  const toggleTask = async () => {
    try {
      const newEnabled = !task.enabled;
      const response = await axios.put(
        `/tasks/${task.id}`,
        {
          enabled: newEnabled,
        },
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        },
      );
      if (response.status === 200) {
        setTasks(
          tasks.map((t) => {
            if (t.id === task.id) {
              return { ...t, enabled: newEnabled };
            }
            return t;
          }),
        );
      }
    } catch (e) {
      // TODO: Emit a global error
      console.log(e);
    }
  };

  const deleteTask = async () => {
    try {
      const response = await axios.delete(`/tasks/${task.id}`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("access_token")}`,
        },
      });
      if (response.status === 204) {
        setTasks([...tasks.filter((t) => t.id !== task.id)]);
      }
    } catch (e) {
      // TODO: Emit a global error
      console.log(e);
    }
  };

  const dropdownButtonStyles =
    "block w-full border-b-[1px] border-border px-4 py-2 text-left hover:bg-primary bg-secondary";

  return (
    <tr>
      <td className="font-medium">{task.name}</td>
      <td className="xxl:pr-10">
        <a className="underline" href={task.url}>
          {task.url}
        </a>
      </td>
      {/* NOTE: Archived Action Column for future usage
        <td>
          <div className="w-min rounded-full bg-info px-4 py-[2px] font-medium text-text-contrast">
            Monitor
          </div>
        </td> 
      */}
      <td>1d 5h 18m</td>
      <td className="overflow-visible">
        <div className="flex items-center justify-between">
          10:49
          <HiDotsVertical
            className="cursor-pointer"
            onClick={() => setOpen(!open)}
          />
        </div>
        <div className="relative" ref={containerRef}>
          {open && (
            <div
              className="absolute right-0 top-3 w-max overflow-hidden rounded-md border-[1px]
                border-border bg-secondary"
            >
              <button
                className={dropdownButtonStyles}
                onClick={() => {
                  setOpen(false);
                  onEditModalOpen();
                }}
              >
                Edit
              </button>
              <button className={dropdownButtonStyles} onClick={toggleTask}>
                {task.enabled ? "Pause Task" : "Run Task"}
              </button>
              <button
                className={`${dropdownButtonStyles} border-b-[0px] text-error`}
                onClick={deleteTask}
              >
                Delete Task
              </button>
            </div>
          )}
        </div>
      </td>
    </tr>
  );
};

export default Task;
