import { useContext, useEffect, useRef } from "react";
// Icons
import { HiDotsVertical } from "react-icons/hi";
// Hooks
import usePopup from "../../hooks/usePopup";
// Types
import { TaskComponent } from "./types";
// Constants
import {
  SECONDS_IN_YEAR,
  SECONDS_IN_MONTH,
  SECONDS_IN_DAYS,
  SECONDS_IN_HOURS,
  SECONDS_IN_MINUTES,
} from "../../constants/time";
// Util
import { axios } from "../../config";
// Context
import { NotificationContext } from "../../hooks/useNotification";

const Task: TaskComponent = ({ task, onEditModalOpen, sectionRef }) => {
  const { open, setOpen, containerRef } = usePopup();
  const addNotification = useContext(NotificationContext);
  const rowRef = useRef<HTMLTableRowElement>(null);

  useEffect(() => {
    const handleResize = () => {
      if (sectionRef.current && rowRef.current && containerRef.current) {
        const { bottom } = rowRef.current.getBoundingClientRect();
        const { right } = sectionRef.current.getBoundingClientRect();
        containerRef.current.style.left = `${right - 150}px`;
        containerRef.current.style.top = `${bottom}px`;
      }
    };

    if (open) {
      handleResize();
      window.addEventListener("resize", handleResize);
    }
    return () => {
      window.removeEventListener("resize", handleResize);
    };
  }, [open]);

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
        addNotification({
          type: "SUCCESS",
          message: `${newEnabled ? "Started" : "Paused"} task: ${task.name}`,
        });
      }
    } catch {
      addNotification({
        type: "ERROR",
        message: "An unexpected error occurred. Please try again later.",
      });
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
        addNotification({
          type: "SUCCESS",
          message: `Successfully deleted task`,
        });
      }
    } catch {
      addNotification({
        type: "ERROR",
        message: "An unexpected error occurred. Please try again later.",
      });
    }
  };

  const computeIntervalString = (seconds: number) => {
    const years = Math.floor(seconds / SECONDS_IN_YEAR);
    seconds = seconds % SECONDS_IN_YEAR;
    const months = Math.floor(seconds / SECONDS_IN_MONTH);
    seconds = seconds % SECONDS_IN_MONTH;
    const days = Math.floor(seconds / SECONDS_IN_DAYS);
    seconds = seconds % SECONDS_IN_DAYS;
    const hours = Math.floor(seconds / SECONDS_IN_HOURS);
    seconds = seconds % SECONDS_IN_HOURS;
    const minutes = Math.floor(seconds / SECONDS_IN_MINUTES);
    seconds = seconds % SECONDS_IN_MINUTES;

    const values = [years, months, days, hours, minutes, seconds];
    const prefixes = ["y", "mo", "d", "h", "m", "s"];
    return prefixes.reduce((prev, cur, i) => {
      if (values[i] <= 0) {
        return prev;
      }
      return `${prev} ${values[i]}${cur}`;
    }, "");
  };

  const dropdownButtonStyles =
    "block w-full border-b-[1px] border-border px-4 py-2 text-left hover:bg-primary bg-secondary";

  return (
    <tr ref={rowRef}>
      <td className="font-medium">{task.name}</td>
      <td className="text-nwrap max-w-[500px] overflow-hidden text-ellipsis xxl:pr-10">
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
      <td>{computeIntervalString(task.interval)}</td>
      <td className="overflow-visible">
        <div className="flex items-center justify-between gap-3">
          {task.nextRun.toLocaleString("en-US")}
          <HiDotsVertical
            className="cursor-pointer"
            onClick={() => setOpen(!open)}
          />
        </div>
        {open && (
          <div
            className="absolute right-0 top-3 w-max overflow-hidden rounded-md border-[1px]
              border-border bg-secondary"
            ref={containerRef}
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
      </td>
    </tr>
  );
};

export default Task;
