import { FunctionComponent } from "react";
import { Task } from "../../types";

interface TaskProps {
  task: Task;
  onEditModalOpen: () => void;
}

export type TaskComponent = FunctionComponent<TaskProps>;
