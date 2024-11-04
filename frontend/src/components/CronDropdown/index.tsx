// Components
import Input from "../Input";
import Dropdown from "../Dropdown";
// Types
import { CronDropdownProps, FormState, Errors } from "./types";
// Constants
import { daysOfWeek, months } from "./constants";

const CronDropdown = <T extends FormState>({
  setOpen,
  formState,
  setFormState,
  showNameField = false,
}: CronDropdownProps<T>) => {
  const updateSchedule = () => {
    const { name, monthDay, hours, minutes } = formState;
    const errors: Errors = {};

    if (name && name.trim().length <= 0) {
      errors.name = "Please enter a name";
    }

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
      setFormState({ ...formState, errors: { ...errors } });
      return;
    }
    setFormState({ ...formState, errors: {} });
    setOpen(false);
  };

  return (
    <div
      className="top-12 grid gap-2 rounded-sm border-[1px] border-border bg-primary p-5 text-left"
      onClick={(e) => e.stopPropagation()}
    >
      {showNameField && (
        <Input
          label="Name"
          inputAttrs={{
            onChange: (e) => {
              formState.name = e.target.value;
            },
          }}
          error={formState.errors.name}
        />
      )}
      <Dropdown
        label="Day of Week:"
        choices={daysOfWeek}
        placeholder="Select a date"
        value={formState.dayOfWeek || ""}
        onChange={(s) => setFormState({ ...formState, dayOfWeek: s })}
      />
      <Dropdown
        label="Month:"
        choices={months}
        placeholder="Select a month"
        value={formState.month || ""}
        onChange={(s) => setFormState({ ...formState, month: s })}
      />
      <div className="grid grid-cols-2 gap-x-6 gap-y-2">
        <Input
          label="Day of Month"
          inputAttrs={{
            value: formState.monthDay,
            type: "number",
            onChange: (e) =>
              setFormState({
                ...formState,
                monthDay: parseInt(e.target.value),
              }),
          }}
          error={formState.errors.monthDay}
        />
        <Input
          label="Hours"
          inputAttrs={{
            value: formState.hours,
            type: "number",
            onChange: (e) =>
              setFormState({ ...formState, hours: parseInt(e.target.value) }),
          }}
          error={formState.errors.hours}
        />
        <Input
          label="Minutes"
          inputAttrs={{
            value: formState.minutes,
            type: "number",
            onChange: (e) =>
              setFormState({ ...formState, minutes: parseInt(e.target.value) }),
          }}
          error={formState.errors.minutes}
        />
        <button
          type="button"
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
