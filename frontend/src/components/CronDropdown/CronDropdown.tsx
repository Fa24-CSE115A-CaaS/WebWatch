import { useState } from "react";

// Components
import Input from "../Input";
import Dropdown from "../Dropdown";
// Types
import { CronDropdownComponent, Errors } from "./types";
// Constants
import { daysOfWeek, months } from "./constants";

const CronDropdown: CronDropdownComponent = ({ setOpen, setCronString }) => {
  const [month, setMonth] = useState<string>("");
  const [dayOfWeek, setDayOfWeek] = useState<string>("");
  const [monthDay, setMonthDay] = useState<number>();
  const [hours, setHours] = useState<number>();
  const [minutes, setMinutes] = useState<number>();
  const [errors, setErrors] = useState<Errors>({});

  const updateSchedule = () => {
    const values = [dayOfWeek, month, monthDay, hours, minutes];
    const errors: Errors = {};

    if (monthDay && (monthDay < 1 || monthDay > 31)) {
      errors.monthDay = "Value between 1-31";
    }

    if (hours && (hours < 0 || hours > 23)) {
      errors.hours = "Value between 0-23";
    }

    if (minutes && (minutes < 0 || minutes > 59)) {
      errors.minutes = "Value between 0-59";
    }

    if (Object.keys(errors).length > 0) {
      setErrors(errors);
      return;
    }
    console.log(values);
    setCronString(values.filter((value) => Boolean(value)).join(", "));
    setOpen(false);
  };

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
        <Input
          label="Day of Month"
          inputAttrs={{
            value: monthDay,
            type: "number",
            onChange: (e) => setMonthDay(parseInt(e.target.value)),
          }}
          error={errors.monthDay}
        />
        <Input
          label="Hours"
          inputAttrs={{
            value: hours,
            type: "number",
            onChange: (e) => setHours(parseInt(e.target.value)),
          }}
          error={errors.hours}
        />
        <Input
          label="Minutes"
          inputAttrs={{
            value: minutes,
            type: "number",
            onChange: (e) => setMinutes(parseInt(e.target.value)),
          }}
          error={errors.minutes}
        />
        <button
          className="w-full self-end rounded-sm bg-accent px-3 py-1 text-text-contrast"
          onClick={updateSchedule}
        >
          Save
        </button>
      </div>
    </div>
  );
};

export default CronDropdown;
