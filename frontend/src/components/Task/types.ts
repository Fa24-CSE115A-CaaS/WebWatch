import { FunctionComponent } from "react";
// Types
import { Task } from "../../types";

interface TaskProps {
  task: Task;
  onEditModalOpen: () => void;
}

export type TaskComponent = FunctionComponent<TaskProps>;
