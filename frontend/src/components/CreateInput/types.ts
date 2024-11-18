import { FormState as CreateInputFormState } from "../CreateInputDropdown/types";

export interface FormState extends CreateInputFormState {
  url: string;
}

export interface FormState {
  errors: {
    [K in keyof FormState]?: string;
  };
}
