import { FunctionComponent, Dispatch, SetStateAction } from "react";

interface InputProps {
  label: string;
  placeholder?: string;
  containerClass?: string;
  value: string;
  onChange: Dispatch<SetStateAction<string>>;
}

type InputComponent = FunctionComponent<InputProps>;

const Input: InputComponent = ({
  label,
  placeholder,
  containerClass,
  value,
  onChange,
}) => {
  return (
    <div className={`w-full ${containerClass}`}>
      <label className="text-sm">{label}</label>
      <input
        className="w-full bg-secondary px-3 py-1 outline-none"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
      />
    </div>
  );
};

export default Input;
