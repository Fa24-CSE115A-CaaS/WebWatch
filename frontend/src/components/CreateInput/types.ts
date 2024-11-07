import { FormState as CronFormState } from "../CronDropdown/types";

export interface FormState extends CronFormState {
  url: string;
}

export interface FormState {
  errors: {
    [K in keyof FormState]?: string;
  };
}
