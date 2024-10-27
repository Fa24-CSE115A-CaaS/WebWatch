import { FaRegClock } from "react-icons/fa6";
import { FaRegBell } from "react-icons/fa";
import { IoSearch } from "react-icons/io5";

const CreateInput = () => {
  return (
    <div
      className="mx-auto my-10 flex h-12 w-[800px] items-center overflow-hidden rounded-full
        border-[1px] border-border bg-primary pl-5 text-text xxl:h-16 xxl:w-[1000px]
        xxl:border-2 xxl:text-xl"
    >
      <IoSearch className="h-5 w-5 xxl:h-6 xxl:w-6" />
      <input
        className="h-full flex-1 border-0 bg-transparent pl-5 text-text outline-none"
        placeholder="Enter a website..."
      />
      <button className="flex items-center justify-center px-5 xxl:px-6">
        <FaRegClock className="h-5 w-5 xxl:h-6 xxl:w-6" />
      </button>
      <button
        className="flex h-full items-center justify-center bg-accent px-5 text-text-contrast
          xxl:px-7"
      >
        <FaRegBell className="h-5 w-5 xxl:h-6 xxl:w-6" />
      </button>
    </div>
  );
};

export default CreateInput;
