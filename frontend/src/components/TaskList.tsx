import { useState } from "react";
// Components
import EditTaskModal from "./EditTaskModal";
import TaskComponent from "./Task";
// Types
import { Task } from "../types";

type TaskListProps = {
  tasks: Task[];
};

type TaskComponent = React.FunctionComponent<TaskListProps>;

const TaskList: TaskComponent = ({ tasks }) => {
  const [editTask, setEditTask] = useState<Task | null>(null);

  return (
    <section
      className="mx-auto mb-10 overflow-hidden rounded-md border-[1px] border-border text-text
        xxl:border-2"
    >
      <table className="w-full table-fixed">
        <thead className="bg-secondary text-left text-sm font-bold xxl:text-lg">
          <tr>
            <th className="w-1/5 xxl:w-[15%]">NAME</th>
            <th>WEBSITE</th>
            <th className="w-[15%]">ACTION</th>
            <th className="w-[15%]">INTERVAL</th>
            <th className="w-[15%]">NEXT CHECK</th>
          </tr>
        </thead>
        <tbody className="xxl:text-xl">
          {tasks.map((task) => (
            <TaskComponent
              task={task}
              key={task.id}
              onEditModalOpen={() => setEditTask(task)}
            />
          ))}
        </tbody>
      </table>
      {tasks.length <= 0 && (
        <div className="w-full bg-primary p-5 text-center xxl:px-8">
          No tasks found.
        </div>
      )}
      {editTask && (
        <EditTaskModal task={editTask} closeModal={() => setEditTask(null)} />
      )}
    </section>
  );
};

export default TaskList;
