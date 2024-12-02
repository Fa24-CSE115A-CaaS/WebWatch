import { useContext, useState } from "react";
// Components
import CreateInputDropdown from "../CreateInputDropdown";
// Hooks
import usePopup from "../../hooks/usePopup";
// Icons
import { FaRegBell } from "react-icons/fa";
import { IoSearch } from "react-icons/io5";
// Types
import { FormState } from "./types";
// Constants
import {
  MAXIMUM_INTERVAL_SECONDS,
  MINIMUM_INTERVAL_SECONDS,
} from "../../constants/tasks";
// Util
import { axios } from "../../config";
// Context
import { NotificationContext } from "../../hooks/useNotification";

const defaultState: FormState = {
  url: "",
  name: "",
  xpath: "",
  interval: NaN,
  errors: {},
};

const CreateInput = () => {
  const { open, setOpen, containerRef } = usePopup();
  const [formState, setFormState] = useState<FormState>(defaultState);
  const addNotification = useContext(NotificationContext);

  const isFormValid = () => {
    const { url, name, interval } = formState;
    let errors: typeof formState.errors = {};

    if (url.trim().length <= 0) {
      errors.url = "Please provide a url";
      addNotification({
        type: "ERROR",
        message: errors.url,
      });
    }

    if (name.trim().length <= 0) {
      errors.name = "Please provide a name";
    }

    if (isNaN(interval)) {
      errors.interval = "Please provide an interval";
    } else if (interval < MINIMUM_INTERVAL_SECONDS) {
      errors.interval = `Interval can not be less than ${MINIMUM_INTERVAL_SECONDS} seconds`;
    } else if (interval > MAXIMUM_INTERVAL_SECONDS) {
      errors.interval = "Interval is too large";
    }

    if (Object.keys(errors).length > 0) {
      setFormState({ ...formState, errors });
      return false;
    }
    return true;
  };

  const onSubmit = async () => {
    if (!isFormValid()) {
      return;
    }

    try {
      const res = await axios.post(
        "/tasks",
        {
          url: formState.url,
          name: formState.name,
          interval: formState.interval,
          xpath: formState.xpath,
        },
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        },
      );

      if (res.status === 201) {
        setFormState({ ...defaultState });
        setOpen(false);
        addNotification({
          type: "SUCCESS",
          message: "Created a new task",
        });
      }
    } catch {
      addNotification({
        type: "ERROR",
        message: "An unexpected error occurred. Please try again later.",
      });
    }
  };

  return (
    <div
      ref={containerRef}
      className="mx-auto my-10 flex h-12 w-[800px] items-center rounded-full border-[1px]
        border-border bg-primary pl-5 text-text xxl:h-16 xxl:border-2 xxl:text-xl"
    >
      <IoSearch className="h-5 w-5 xxl:h-6 xxl:w-6" />
      <input
        className="h-full flex-1 border-0 bg-transparent pl-5 text-text outline-none"
        placeholder="Enter a website..."
        value={formState.url}
        onChange={(e) => setFormState({ ...formState, url: e.target.value })}
        onFocus={() => setOpen(true)}
      />
      <div className="relative flex items-center justify-center px-5 xxl:px-6">
        {open && (
          <div className="absolute right-0 top-8 w-80 xxl:top-16 xxl:w-96">
            <CreateInputDropdown
              formState={formState}
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
