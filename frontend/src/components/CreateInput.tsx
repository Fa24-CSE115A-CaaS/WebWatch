import { useState } from "react";
// Components
import CronDropdown from "./CronDropdown/CronDropdown";
// Hooks
import usePopup from "../hooks/usePopup";
// Icons
import { FaRegClock } from "react-icons/fa6";
import { FaRegBell } from "react-icons/fa";
import { IoSearch } from "react-icons/io5";

const CreateInput = () => {
  const { open, setOpen, containerRef } = usePopup();
  const [cronString, setCronString] = useState("");

  return (
    <div
      className="mx-auto my-10 flex h-12 w-[800px] items-center rounded-full border-[1px]
        border-border bg-primary pl-5 text-text xxl:h-16 xxl:w-[1000px] xxl:border-2
        xxl:text-xl"
    >
      <IoSearch className="h-5 w-5 xxl:h-6 xxl:w-6" />
      <input
        className="h-full flex-1 border-0 bg-transparent pl-5 text-text outline-none"
        placeholder="Enter a website..."
      />
      <div
        className="relative flex items-center justify-center px-5 xxl:px-6"
        onClick={() => setOpen(!open)}
        ref={containerRef}
      >
        <button className="flex items-center justify-center gap-2">
          <FaRegClock className="h-5 w-5 xxl:h-6 xxl:w-6" />
          {cronString && <p>{cronString}</p>}
        </button>

        {open && (
          <CronDropdown setOpen={setOpen} setCronString={setCronString} />
        )}
      </div>
      <button
        className="flex h-full items-center justify-center rounded-r-full bg-accent px-5
          text-text-contrast xxl:px-7"
      >
        <FaRegBell className="h-5 w-5 xxl:h-6 xxl:w-6" />
      </button>
    </div>
  );
};

export default CreateInput;
