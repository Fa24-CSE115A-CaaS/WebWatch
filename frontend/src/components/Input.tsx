import {
  FunctionComponent,
  InputHTMLAttributes,
} from "react";

interface InputProps {
  label: string;
  containerClass?: string;
  inputAttrs: InputHTMLAttributes<HTMLInputElement>;
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
      <label className="text-sm">{label}</label>
      <input
        className="w-full bg-secondary px-3 py-1 outline-none"
        {...inputAttrs}
      />
      {error && <p className="text-xs text-error">{error}</p>}
    </div>
  );
};

export default Input;
