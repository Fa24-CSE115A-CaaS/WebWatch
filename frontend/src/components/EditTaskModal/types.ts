import { FunctionComponent } from "react";
// Types
import { Task } from "../../types";
import { FormState as CronDropdownFormState } from "../CronDropdown/types";

export interface FormState extends CronDropdownFormState {
  name: string;
  url: string;
  notificationOptions: string[];
  discordUrl: string;
  slackUrl: string;
}

export interface FormState {
  errors: { [K in keyof FormState]?: string };
}

interface EditTaskModalProps {
  task: Task;
  closeModal: () => void;
}

export type EditTaskModalComponent = FunctionComponent<EditTaskModalProps>;
