import { FunctionComponent, MouseEventHandler } from "react";
// Components
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
            "w-6 h-6 xxl:w-8 xxl:h-8 accent-accent hover:accent-accent-hover cursor-pointer",
          defaultChecked: value,
          onClick,
        }}
      />
      <p className="xxl:text-xl">{label}</p>
    </div>
  );
};

export default EditCheckbox;
