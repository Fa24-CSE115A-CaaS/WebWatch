import { FunctionComponent, RefObject } from "react";
// Types
import { Task } from "../../types";

interface TaskProps {
  task: Task;
  onEditModalOpen: () => void;
  sectionRef: RefObject<HTMLDivElement>;
}

export type TaskComponent = FunctionComponent<TaskProps>;
