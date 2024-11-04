// Components
import TaskList from "../components/TaskList";
import CreateInput from "../components/CreateInput";
import EditTaskModal from "../components/EditTaskModal";
// Constants
import { dummyTasks } from "../constants/dummyTasks";

const Tasks = () => {
  return (
    <main>
      <CreateInput />
      <TaskList tasks={dummyTasks} />
      <EditTaskModal />
    </main>
  );
};

export default Tasks;
