import { useState } from "react";
// Components
import Input from "../Input";
import EditCheckbox from "./EditCheckbox";
import CronDropdown from "../CronDropdown";
// Types
import { FormState } from "./types";

const NOTIFICATION_OPTS = ["EMAIL", "DISCORD", "SLACK"];

const EditTaskModal = () => {
  const [formState, setFormState] = useState<FormState>({
    name: "",
    url: "",
    notificationOptions: [],
    discordUrl: "",
    slackUrl: "",
    dayOfWeek: "",
    month: "",
    errors: {},
  });

  return (
    <div
      className="modal fixed top-0 flex h-screen w-screen items-center justify-center bg-black
        bg-opacity-60 text-text"
      onClick={() => {}}
    >
      <form
        className="w-[1000px] rounded-lg bg-primary p-8"
        onClick={(e) => e.stopPropagation()}
      >
        <h1 className="mb-10 text-2xl">Edit Task</h1>
        <div className="grid grid-cols-2 gap-10">
          <div>
            <Input label="Task Name" containerClass="mb-3" />
            <Input label="Target URL" containerClass="mb-3" />
            <div className="my-5">
              <h3 className="text-xl">Notfication Options</h3>
              {NOTIFICATION_OPTS.map((opt) => {
                const notifOpt = formState.notificationOptions;
                const notifLoc = notifOpt.indexOf(opt);
                const titleOpt = opt.charAt(0) + opt.slice(1).toLowerCase();
                return (
                  <EditCheckbox
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
            </div>
            <Input label="Discord Webhook URL" containerClass="mb-3" />
            <Input label="Slack Webhook URL" containerClass="mb-3" />
          </div>
          <div>
            <Input label="Formatted Schedule" containerClass="mb-3" />
            <div className="mx-7 my-5">
              <CronDropdown<FormState>
                formState={formState}
                setFormState={setFormState}
                setOpen={() => {}}
              />
            </div>
            <button
              className="w-full rounded-sm bg-accent py-3 text-center text-text-contrast
                hover:bg-accent-hover"
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
