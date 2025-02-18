// Components
import Input from "../Input";
// Types
import { CreateInputDropdownProps, FormState } from "./types";

const CreateInputDropdown = <T extends FormState>({
  formState,
  setFormState,
}: CreateInputDropdownProps<T>) => {
  return (
    <div
      className="grid gap-2 rounded-sm border-[1px] border-border bg-primary p-5 text-left"
      onClick={(e) => e.stopPropagation()}
    >
      <Input
        label="Name"
        inputAttrs={{
          onChange: (e) => {
            setFormState({ ...formState, name: e.target.value });
          },
          value: formState.name,
        }}
        error={formState.errors.name}
      />
      <Input
        label="Interval"
        inputAttrs={{
          type: "number",
          onChange: (e) => {
            setFormState({
              ...formState,
              interval: parseInt(e.target.value),
            });
          },
          value: isNaN(formState.interval) ? "" : formState.interval,
          placeholder: "Enter an interval in seconds",
        }}
        error={formState.errors.interval}
      />
      <Input
        label="XPath"
        inputAttrs={{
          onChange: (e) => {
            setFormState({
              ...formState,
              xpath: e.target.value,
            });
          },
          value: formState.xpath,
          placeholder: "Enter an xpath",
        }}
        error={formState.errors.xpath}
      />
    </div>
  );
};

export default CreateInputDropdown;
