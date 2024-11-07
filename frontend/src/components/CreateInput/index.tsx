import { useContext, useState } from "react";
// Components
import CronDropdown from "../CronDropdown";
// Hooks
import usePopup from "../../hooks/usePopup";
// Icons
import { FaRegBell } from "react-icons/fa";
import { IoSearch, IoSettingsOutline } from "react-icons/io5";
// Types
import { TaskResponse } from "../../types";
import { FormState } from "./types";
// Util
import { axios } from "../../config";
import { TasksPageContext } from "../../pages/Tasks";

const defaultState: FormState = {
  url: "",
  name: "",
  month: "",
  dayOfWeek: "",
  errors: {},
};

const CreateInput = () => {
  const { tasks, setTasks } = useContext(TasksPageContext)!;
  const { open, setOpen, containerRef } = usePopup();
  const [formState, setFormState] = useState<FormState>(defaultState);

  const onSubmit = async () => {
    try {
      const token = localStorage.getItem("access_token");
      const res = await axios.post(
        "/tasks",
        {
          url: formState.url,
          name: formState.name,
          user_id: 1,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        },
      );

      if (res.status === 201) {
        const data = res.data as TaskResponse;
        setFormState({ ...defaultState });
        setTasks([
          ...tasks,
          {
            id: data.id,
            name: data.name,
            content: data.content,
            url: data.url,
            discordUrl: data.discord_url,
            enabledNotificationOptions: data.enabled_notification_options,
            enabled: data.enabled,
          },
        ]);
      }
    } catch {}
  };

  return (
    <div
      className="mx-auto my-10 flex h-12 w-[800px] items-center rounded-full border-[1px]
        border-border bg-primary pl-5 text-text xxl:h-16 xxl:border-2 xxl:text-xl"
    >
      <IoSearch className="h-5 w-5 xxl:h-6 xxl:w-6" />
      <input
        className="h-full flex-1 border-0 bg-transparent pl-5 text-text outline-none"
        placeholder="Enter a website..."
        value={formState.url}
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
          <div className="absolute right-0 top-12 w-80 xxl:top-16 xxl:w-96">
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
          text-text-contrast transition-all duration-100 ease-out hover:bg-accent-hover
          xxl:px-7"
        onClick={onSubmit}
      >
        <FaRegBell className="h-5 w-5 xxl:h-6 xxl:w-6" />
      </button>
    </div>
  );
};

export default CreateInput;
