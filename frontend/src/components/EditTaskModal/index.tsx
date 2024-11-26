import { FormEventHandler, useContext, useState } from "react";
import { axios } from "../../config";
// Components
import Input from "../Input";
import EditCheckbox from "./EditCheckbox";
// Types
import { EditTaskModalComponent, FormState } from "./types";
// Icons
import { RxCross2 } from "react-icons/rx";
// Constants
import {
  MAXIMUM_INTERVAL_SECONDS,
  MINIMUM_INTERVAL_SECONDS,
} from "../../constants/tasks";
// Context
import { NotificationContext } from "../../hooks/useNotification";

const NOTIFICATION_OPTS = ["EMAIL", "DISCORD", "SLACK"];

const EditTaskModal: EditTaskModalComponent = ({ task, closeModal }) => {
  const [formState, setFormState] = useState<FormState>({
    name: task.name,
    url: task.url,
    notificationOptions: task.enabledNotificationOptions,
    discordUrl: task.discordUrl || "",
    slackUrl: "",
    interval: task.interval,
    errors: {},
  });
  const addNotification = useContext(NotificationContext);

  const { name, url, notificationOptions, discordUrl, slackUrl, interval } =
    formState;

  const handleFormSubmit: FormEventHandler<HTMLFormElement> = async (e) => {
    e.preventDefault();
    let errors: typeof formState.errors = {};

    if (name.trim().length <= 0) {
      errors.name = "Please enter a name";
    }

    if (url.trim().length <= 0) {
      errors.url = "Please enter a url";
    }

    if (isNaN(interval)) {
      errors.interval = "Please provide an interval";
    } else if (interval < MINIMUM_INTERVAL_SECONDS) {
      errors.interval = `Interval can not be less than ${MINIMUM_INTERVAL_SECONDS} seconds`;
    } else if (interval > MAXIMUM_INTERVAL_SECONDS) {
      errors.interval = "Interval is too large";
    }

    if (notificationOptions.length <= 0) {
      errors.notificationOptions =
        "Please select at least one notification option";
    }

    if (
      notificationOptions.includes("DISCORD") &&
      discordUrl.trim().length <= 0
    ) {
      errors.discordUrl = "Please enter a Discord webhook url";
    }

    if (notificationOptions.includes("SLACK") && slackUrl.trim().length <= 0) {
      errors.slackUrl = "Please enter a Slack webhook url";
    }

    if (Object.keys(errors).length > 0) {
      setFormState({ ...formState, errors });
      return;
    }

    try {
      const response = await axios.put(
        `/tasks/${task.id}`,
        {
          name,
          url,
          enabled_notification_options: notificationOptions,
          interval,
          discord_url: discordUrl,
          slack_url: slackUrl,
        },
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        },
      );

      if (response.status === 200) {
        closeModal();
        addNotification({
          type: "SUCCESS",
          message: `Modified task: ${task.name}`,
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
      className="modal fixed left-0 top-0 flex h-screen w-screen items-center justify-center
        bg-black bg-opacity-60 text-text"
      onClick={closeModal}
    >
      <form
        className="relative w-[1000px] rounded-lg bg-primary p-8 xxl:w-[1200px] xxl:p-10"
        onSubmit={handleFormSubmit}
        onClick={(e) => e.stopPropagation()}
      >
        <h1 className="mb-10 text-2xl xxl:text-3xl">Edit Task</h1>
        <button
          className="absolute right-0 top-0 bg-transparent p-5"
          onClick={closeModal}
        >
          <RxCross2 size={20} />
        </button>
        <div className="grid grid-cols-2 gap-10 xxl:gap-14">
          <div>
            <h3 className="mb-5 text-xl xxl:text-2xl">General Info</h3>
            <Input
              label="Task Name"
              containerClass="mb-3"
              inputAttrs={{
                value: name,
                onChange: (e) =>
                  setFormState({ ...formState, name: e.target.value }),
              }}
              error={formState.errors.name}
            />
            <Input
              label="Target URL"
              containerClass="mb-3"
              inputAttrs={{
                value: url,
                onChange: (e) =>
                  setFormState({ ...formState, url: e.target.value }),
              }}
              error={formState.errors.url}
            />
            <Input
              label="Interval"
              containerClass="mb-3"
              inputAttrs={{
                value: isNaN(interval) ? "" : interval,
                onChange: (e) =>
                  setFormState({
                    ...formState,
                    interval: parseInt(e.target.value),
                  }),
                placeholder: "Enter an interval in seconds",
              }}
              error={formState.errors.interval}
            />
          </div>
          <div>
            <h3 className="mb-5 text-xl xxl:text-2xl">Notfication Options</h3>
            <div className="mb-5">
              {NOTIFICATION_OPTS.map((opt) => {
                const notifOpt = notificationOptions;
                const notifLoc = notifOpt.indexOf(opt);
                const titleOpt = opt.charAt(0) + opt.slice(1).toLowerCase();
                return (
                  <EditCheckbox
                    key={opt}
                    label={titleOpt}
                    value={notifOpt.includes(opt)}
                    onClick={() => {
                      if (notifLoc >= 0) {
                        setFormState({
                          ...formState,
                          notificationOptions: notifOpt.filter(
                            (v) => v !== opt,
                          ),
                        });
                      } else {
                        setFormState({
                          ...formState,
                          notificationOptions: [...notifOpt, opt],
                        });
                      }
                    }}
                  />
                );
              })}
              {formState.errors.notificationOptions && (
                <p className="text-sm text-error">
                  {formState.errors.notificationOptions}
                </p>
              )}
            </div>
            <Input
              label="Discord Webhook URL"
              containerClass="mb-3"
              inputAttrs={{
                value: discordUrl,
                onChange: (e) =>
                  setFormState({ ...formState, discordUrl: e.target.value }),
              }}
              error={formState.errors.discordUrl}
            />
            <Input
              label="Slack Webhook URL"
              containerClass="mb-3"
              inputAttrs={{
                value: slackUrl,
                onChange: (e) =>
                  setFormState({ ...formState, slackUrl: e.target.value }),
              }}
              error={formState.errors.slackUrl}
            />
            <button
              className="w-full rounded-sm bg-accent py-3 text-center text-text-contrast transition-all
                duration-100 ease-out hover:bg-accent-hover xxl:text-xl"
            >
              Update Task
            </button>
          </div>
        </div>
      </form>
    </div>
  );
};

export default EditTaskModal;
