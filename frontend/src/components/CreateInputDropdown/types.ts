import { Dispatch, SetStateAction } from "react";

export interface FormState {
  name: string;
  seconds: number;
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
