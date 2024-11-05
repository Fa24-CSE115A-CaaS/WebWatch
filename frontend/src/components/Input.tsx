import { FunctionComponent, InputHTMLAttributes } from "react";

interface InputProps {
  label: string;
  containerClass?: string;
  inputAttrs?: InputHTMLAttributes<HTMLInputElement>;
  error?: string;
}

type InputComponent = FunctionComponent<InputProps>;

const Input: InputComponent = ({
  label,
  containerClass,
  inputAttrs,
  error,
}) => {
  return (
    <div className={`w-full ${containerClass}`}>
      <label className="mb-2 block text-sm xxl:text-lg">{label}</label>
      <input
        className="w-full bg-secondary px-3 py-1 outline-none xxl:text-xl"
        {...inputAttrs}
      />
      {error && <p className="text-xs text-error xxl:text-sm">{error}</p>}
    </div>
  );
};

export default Input;
