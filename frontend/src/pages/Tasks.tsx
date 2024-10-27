// Components
import TaskList from "../components/TaskList";
import CreateInput from "../components/CreateInput";
// Constants
import { dummyTasks } from "../constants/dummyTasks";

const Tasks = () => {
  return (
    <main>
      <CreateInput />
      <TaskList tasks={dummyTasks} />
    </main>
  );
};

export default Tasks;
