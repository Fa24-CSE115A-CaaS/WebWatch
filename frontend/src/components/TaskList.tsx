import { useState, useRef } from "react";
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
  const sectionRef = useRef<HTMLDivElement>(null);

  return (
    <section
      className="mx-auto mb-10 overflow-x-auto rounded-md border-[1px] border-border text-text
        xxl:border-2"
      ref={sectionRef}
    >
      <table className="w-full">
        <thead className="text-nowrap bg-secondary text-left text-sm font-bold xxl:text-lg">
          <tr>
            <th className="w-1/5 rounded-tl-md xxl:w-[15%]">NAME</th>
            <th className="w-1/5">WEBSITE</th>
            {/* NOTE: Archived Action Column for future usage 
              <th className="w-[15%]">ACTION</th> 
            */}
            <th className="w-[15%]">INTERVAL</th>
            <th className="w-[20%] rounded-tr-md">NEXT CHECK</th>
          </tr>
        </thead>
        <tbody className="xxl:text-xl">
          {tasks.map((task) => (
            <TaskComponent
              task={task}
              key={task.id}
              sectionRef={sectionRef}
              onEditModalOpen={() => setEditTask(task)}
            />
          ))}
        </tbody>
      </table>
      {tasks.length <= 0 && (
        <div className="w-full rounded-b-md bg-primary p-5 text-center xxl:px-8">
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
