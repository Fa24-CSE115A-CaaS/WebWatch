import { FunctionComponent } from "react";
// Types
import { Task } from "../../types";

export interface FormState {
  name: string;
  url: string;
  notificationOptions: string[];
  discordUrl: string;
  slackUrl: string;
  interval: number;
  xpath: string;
}

export interface FormState {
  errors: { [K in keyof FormState]?: string };
}

interface EditTaskModalProps {
  task: Task;
  closeModal: () => void;
}

export type EditTaskModalComponent = FunctionComponent<EditTaskModalProps>;
