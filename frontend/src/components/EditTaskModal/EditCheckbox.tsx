import { FunctionComponent, MouseEventHandler } from "react";
import Input from "../Input";

interface EditCheckboxProps {
  label: string;
  value: boolean;
  onClick: MouseEventHandler<HTMLInputElement>;
}

type EditCheckboxComponent = FunctionComponent<EditCheckboxProps>;

const EditCheckbox: EditCheckboxComponent = ({ label, value, onClick }) => {
  return (
    <div className="flex items-center gap-5">
      <Input
        label=""
        containerClass="w-min"
        inputAttrs={{
          type: "checkbox",
          className:
            "w-6 h-6 accent-accent hover:accent-accent-hover cursor-pointer",
          checked: value,
          onClick,
        }}
      />
      <p>{label}</p>
    </div>
  );
};

export default EditCheckbox;
