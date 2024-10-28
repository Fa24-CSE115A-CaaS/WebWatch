import { FunctionComponent, Dispatch, SetStateAction } from "react";
import { FaChevronDown, FaChevronUp } from "react-icons/fa6";
import usePopup from "../hooks/usePopup";

interface DropdownProps {
  label: string;
  placeholder: string;
  choices: string[];
  containerClass?: string;
  value: string;
  onChange: Dispatch<SetStateAction<string>>;
}

type DropdownComponent = FunctionComponent<DropdownProps>;

const Dropdown: DropdownComponent = ({
  label,
  choices,
  placeholder,
  containerClass,
  value,
  onChange,
}) => {
  const { open, setOpen, containerRef } = usePopup();

  return (
    <div className={`w-full ${containerClass}`} ref={containerRef}>
      <label className="text-sm">{label}</label>
      <div
        className="flex cursor-pointer items-center bg-secondary px-3 py-1"
        onClick={() => setOpen(!open)}
      >
        <p className="flex-1">{value || placeholder}</p>
        {open ? <FaChevronUp size={15} /> : <FaChevronDown size={15} />}
      </div>
      {open && (
        <div className="relative">
          <div className="absolute top-2 w-full rounded-md border-[1px] border-border bg-secondary">
            {choices.map((choice, i) => (
              <div
                key={i}
                className="px-3 py-1 transition-colors duration-100 ease-out hover:bg-background"
                onClick={() => {
                  onChange(choice);
                  setOpen(false);
                }}
              >
                <p>{choice}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default Dropdown;
