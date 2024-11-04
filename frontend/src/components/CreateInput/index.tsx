import { useState } from "react";
// Components
import CronDropdown from "../CronDropdown";
// Hooks
import usePopup from "../../hooks/usePopup";
import { axios } from "../../config";
// Icons
import { FaRegBell } from "react-icons/fa";
import { IoSearch, IoSettingsOutline } from "react-icons/io5";
// Types
import { Task } from "../../types";
import { FormState } from "./types";

const CreateInput = () => {
  const { open, setOpen, containerRef } = usePopup();
  const [formState, setFormState] = useState<FormState>({
    url: "",
    name: "",
    month: "",
    dayOfWeek: "",
    errors: {},
  });

  const onSubmit = async () => {
    try {
      const res = await axios.post("/tasks/create", {
        url: formState.url,
        name: formState.name,
      });

      if (res.status === 201) {
        res.data as Task;
      }
    } catch {}
  };

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
        onChange={(e) => setFormState({ ...formState, url: e.target.value })}
      />
      <div
        className="relative flex items-center justify-center px-5 xxl:px-6"
        onClick={() => setOpen(!open)}
        ref={containerRef}
      >
        <button className="flex items-center justify-center gap-2">
          <IoSettingsOutline className="h-5 w-5 xxl:h-6 xxl:w-6" />
          {formState.name && <p>{formState.name}</p>}
        </button>

        {open && (
          <div className="absolute right-0 top-12 w-80">
            <CronDropdown
              setOpen={setOpen}
              formState={formState}
              showNameField={true}
              setFormState={setFormState}
            />
          </div>
        )}
      </div>
      <button
        className="flex h-full items-center justify-center rounded-r-full bg-accent px-5
          text-text-contrast xxl:px-7"
        onClick={onSubmit}
      >
        <FaRegBell className="h-5 w-5 xxl:h-6 xxl:w-6" />
      </button>
    </div>
  );
};

export default CreateInput;
