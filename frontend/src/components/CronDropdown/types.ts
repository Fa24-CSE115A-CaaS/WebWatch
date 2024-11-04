import { Dispatch, SetStateAction } from "react";

export interface FormState {
  name: string;
  dayOfWeek: string;
  month: string;
  monthDay?: number;
  hours?: number;
  minutes?: number;
}

export type Errors = { [K in keyof FormState]?: string };

export interface FormState {
  errors: Errors;
}

export interface CronDropdownProps<T> {
  setOpen: Dispatch<SetStateAction<boolean>>;
  formState: T;
  setFormState: Dispatch<SetStateAction<T>>;
}
