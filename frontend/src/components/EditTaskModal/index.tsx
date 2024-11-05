import { FormEventHandler, useState } from "react";
// Components
import Input from "../Input";
import EditCheckbox from "./EditCheckbox";
import CronDropdown from "../CronDropdown";
// Types
import { EditTaskModalComponent, FormState } from "./types";

const NOTIFICATION_OPTS = ["EMAIL", "DISCORD", "SLACK"];

const EditTaskModal: EditTaskModalComponent = ({ task, closeModal }) => {
  const [formState, setFormState] = useState<FormState>({
    name: task.name,
    url: task.url,
    notificationOptions: task.enabledNotificationOptions,
    discordUrl: task.discordUrl || "",
    slackUrl: "",
    dayOfWeek: "",
    month: "",
    errors: {},
  });

  const { name, url, notificationOptions, discordUrl, slackUrl } = formState;

  const handleFormSubmit: FormEventHandler<HTMLFormElement> = (e) => {
    e.preventDefault();
  };

  return (
    <div
      className="modal fixed left-0 top-0 flex h-screen w-screen items-center justify-center
        bg-black bg-opacity-60 text-text"
      onClick={closeModal}
    >
      <form
        className="w-[1000px] rounded-lg bg-primary p-8 xxl:w-[1200px] xxl:p-10"
        onSubmit={handleFormSubmit}
        onClick={(e) => e.stopPropagation()}
      >
        <h1 className="mb-10 text-2xl xxl:text-3xl">Edit Task</h1>
        <div className="grid grid-cols-2 gap-10 xxl:gap-14">
          <div>
            <Input
              label="Task Name"
              containerClass="mb-3"
              inputAttrs={{
                value: name,
                onChange: (e) =>
                  setFormState({ ...formState, name: e.target.value }),
              }}
            />
            <Input
              label="Target URL"
              containerClass="mb-3"
              inputAttrs={{
                value: url,
                onChange: (e) =>
                  setFormState({ ...formState, url: e.target.value }),
              }}
            />
            <div className="my-5">
              <h3 className="mb-2 text-xl xxl:text-2xl">Notfication Options</h3>
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
            </div>
            <Input
              label="Discord Webhook URL"
              containerClass="mb-3"
              inputAttrs={{
                value: discordUrl,
                onChange: (e) =>
                  setFormState({ ...formState, discordUrl: e.target.value }),
              }}
            />
            <Input
              label="Slack Webhook URL"
              containerClass="mb-3"
              inputAttrs={{
                value: slackUrl,
                onChange: (e) =>
                  setFormState({ ...formState, slackUrl: e.target.value }),
              }}
            />
          </div>
          <div>
            <Input label="Formatted Schedule" containerClass="mb-3" />
            <div className="mx-7 my-5 xxl:mx-10 xxl:my-7">
              <CronDropdown<FormState>
                formState={formState}
                setFormState={setFormState}
                setOpen={() => {}}
              />
            </div>
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
