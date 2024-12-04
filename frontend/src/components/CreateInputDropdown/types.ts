import { Dispatch, SetStateAction } from "react";

export interface FormState {
  name: string;
  interval: number;
  xpath: string;
}

export interface FormState {
  errors: {
    [K in keyof FormState]?: string;
  };
}

export interface CreateInputDropdownProps<T> {
  formState: T;
  setFormState: Dispatch<SetStateAction<T>>;
}
