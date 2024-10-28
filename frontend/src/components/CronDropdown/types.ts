import { Dispatch, FunctionComponent, SetStateAction } from "react";

interface CronDropdownProps {
  setOpen: Dispatch<SetStateAction<boolean>>;
}

export type CronDropdownComponent = FunctionComponent<CronDropdownProps>;
