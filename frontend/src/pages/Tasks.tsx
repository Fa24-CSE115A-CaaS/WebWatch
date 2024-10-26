import TaskList from "../components/TaskList";
import { dummyTasks } from "../constants/dummyTasks";

const Tasks = () => {
  return <TaskList tasks={dummyTasks} />;
};

export default Tasks;
