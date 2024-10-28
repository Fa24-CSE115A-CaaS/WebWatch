import { useContext } from "react";
import { CreateInputFormContext } from "../CreateInput";
// Components
import Input from "../Input";
import Dropdown from "../Dropdown";
// Types
import { CronDropdownComponent } from "./types";
// Constants
import { daysOfWeek, months } from "./constants";

const CronDropdown: CronDropdownComponent = ({ setOpen }) => {
  const {
    month,
    setMonth,
    dayOfWeek,
    setDayOfWeek,
    monthDay,
    setMonthDay,
    hours,
    setHours,
    minutes,
    setMinutes,
  } = useContext(CreateInputFormContext)!;

  return (
    <div
      className="absolute right-0 top-12 grid w-80 gap-2 rounded-sm border-[1px] border-border
        bg-primary p-5 text-left"
      onClick={(e) => e.stopPropagation()}
    >
      <Dropdown
        label="Day of Week:"
        choices={daysOfWeek}
        placeholder="Select a date"
        value={dayOfWeek}
        onChange={setDayOfWeek}
      />
      <Dropdown
        label="Month:"
        choices={months}
        placeholder="Select a month"
        value={month}
        onChange={setMonth}
      />
      <div className="grid grid-cols-2 gap-x-6 gap-y-2">
        <Input label="Day of Month" value={monthDay} onChange={setMonthDay} />
        <Input label="Hours" value={hours} onChange={setHours} />
        <Input label="Minutes" value={minutes} onChange={setMinutes} />
        <button
          className="w-full self-end rounded-sm bg-accent px-3 py-1 text-text-contrast"
          onClick={() => {
            setOpen(false);
          }}
        >
          Save
        </button>
      </div>
    </div>
  );
};

export default CronDropdown;
