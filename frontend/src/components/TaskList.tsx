import { Task } from "../types";
// Icons
import { HiDotsVertical } from "react-icons/hi";

type TaskListProps = {
  tasks: Task[];
};

type TaskComponent = React.FunctionComponent<TaskListProps>;

const TaskList: TaskComponent = ({ tasks }) => {
  return (
    <section
      className="xxl:w-[1500px] xxl:border-2 mx-auto mt-10 overflow-hidden rounded-md
        border-[1px] border-border text-text xl:w-[1200px]"
    >
      <table className="w-full table-fixed">
        <thead className="xxl:text-lg bg-secondary text-left text-sm font-bold">
          <tr>
            <th className="xxl:w-[15%] w-1/5">NAME</th>
            <th>WEBSITE</th>
            <th className="w-[15%]">ACTION</th>
            <th className="w-[15%]">INTERVAL</th>
            <th className="w-[15%]">NEXT CHECK</th>
          </tr>
        </thead>
        <tbody className="xxl:text-xl">
          {tasks.map((task) => (
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
              <td>
                <div className="flex items-center justify-between">
                  10:49
                  <HiDotsVertical className="cursor-pointer" />
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
};

export default TaskList;
