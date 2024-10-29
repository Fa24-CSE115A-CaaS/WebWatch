import { Dispatch, FunctionComponent, SetStateAction } from "react";

interface CronDropdownProps {
  setOpen: Dispatch<SetStateAction<boolean>>;
  setCronString: Dispatch<SetStateAction<string>>;
}

type ErrorKeys = 'dayOfWeek' | 'month' | 'monthDay' | 'hours' | 'minutes';

export type Errors = { 
  [K in ErrorKeys]?: string;
}

export type CronDropdownComponent = FunctionComponent<CronDropdownProps>;
