// Icons
import { HiDotsVertical } from "react-icons/hi";
// Hooks
import usePopup from "../../hooks/usePopup";
// Types
import { TaskComponent } from "./types";

const Task: TaskComponent = ({ task, onEditModalOpen }) => {
  const { open, setOpen, containerRef } = usePopup();

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
      <td>
        <div className="w-min rounded-full bg-info px-4 py-[2px] font-medium text-text-contrast">
          Monitor
        </div>
      </td>
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
              <button className={dropdownButtonStyles}>
                {task.enabled ? "Pause Task" : "Run Task"}
              </button>
              <button
                className={`${dropdownButtonStyles} border-b-[0px] text-error`}
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
