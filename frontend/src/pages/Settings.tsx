import useAuth from "../hooks/useAuth";
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
// import { FaUserCircle } from "react-icons/fa";

import { axios } from "../config";
//import { useMediaQuery } from "react-responsive";

const Settings = () => {
  const { isTokenValid } = useAuth({ redirectToAuth: true });
  //const [activeTab, setActiveTab] = useState("vertical-tab-1");
  const navigate = useNavigate();
  /*const isTabletOrMobile = useMediaQuery({
    query: "(min-width: 640px)",
  }); */

  useEffect(() => {
    if (!isTokenValid) {
      return;
    }
  }, [isTokenValid, navigate]);

  /*const handleTabClick = (tabId: string) => {
    setActiveTab(tabId);
  }; */

  let canSubmitEmail = false;
  let canSubmitPassword = false;

  const handlePasswordResetSubmission = () => {
    if (!canSubmitPassword) {
      handlePasswordInputEvents();
      return;
    }

    const payload = {
      new_password: (
        document.querySelector(
          'input[name="password-reset-password"]',
        ) as HTMLInputElement
      ).value,
      confirm_password: (
        document.querySelector(
          'input[name="password-reset-confirm-password"]',
        ) as HTMLInputElement
      ).value,
    };

    const password_reset_error_message = document.getElementById(
      "password-reset-error-message",
    ) as HTMLParagraphElement;

    axios
      .post("/users/reset_password", payload, {
        headers: {
          accept: "application/json",
          Authorization: "Bearer " + localStorage.getItem("access_token"),
        },
      })
      .then((response) => {
        if (response.status === 200) {
          password_reset_error_message.innerText =
            "Password reset successfully";
        }
      })
      .catch(() => {
        password_reset_error_message.innerText = "Password reset failed";
      });
  };

  const handlePasswordInputEvents = () => {
    {
      const password_reset_password = document.querySelector(
        'input[name="password-reset-password"]',
      ) as HTMLInputElement;
      const password_reset_confirm_password = document.querySelector(
        'input[name="password-reset-confirm-password"]',
      ) as HTMLInputElement;
      const password_reset_error_message = document.getElementById(
        "password-reset-error-message",
      ) as HTMLParagraphElement;
      const status_changer_error = (message: string) => {
        password_reset_password.classList.add("border-error");
        password_reset_confirm_password.classList.add("border-error");
        password_reset_error_message.innerText = message;
        canSubmitPassword = false;
      };

      if (
        password_reset_password.value !== password_reset_confirm_password.value
      ) {
        status_changer_error("Passwords do not match");
      } else if (password_reset_password.value.length < 8) {
        status_changer_error("Password must be at least 8 characters long");
      } else if (!password_reset_confirm_password.value.match(/[0-9]/)) {
        status_changer_error("Password must contain at least one number");
      } else if (!password_reset_confirm_password.value.match(/[a-z]/)) {
        status_changer_error(
          "Password must contain at least one lowercase letter",
        );
      } else if (!password_reset_confirm_password.value.match(/[A-Z]/)) {
        status_changer_error(
          "Password must contain at least one uppercase letter",
        );
      } else if (!password_reset_confirm_password.value.match(/[A-Za-z0-9]/)) {
        status_changer_error(
          "Password must contain at least one special character",
        );
      } else {
        password_reset_password.classList.remove("border-error");
        password_reset_confirm_password.classList.remove("border-error");
        password_reset_error_message.innerText = "";
        canSubmitPassword = true;
      }
    }
  };

  const handleEmailChangeEvents = () => {
    const email = document.querySelector(
      'input[type="email"]',
    ) as HTMLInputElement;
    const email_error_message = document.getElementById(
      "email-error-message",
    ) as HTMLParagraphElement;
    const status_changer_error = (message: string) => {
      email.classList.add("border-error");
      email_error_message.innerText = message;
      canSubmitEmail = false;
    };

    if (
      !email.value.match(/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/)
    ) {
      status_changer_error("Invalid email address");
    } else {
      email.classList.remove("border-error");
      email_error_message.innerText = "";
      canSubmitEmail = true;
    }
  };

  const handleEmailChangeSubmission = () => {
    if (!canSubmitEmail) {
      handleEmailChangeEvents();
      return;
    }
    const email_error_message = document.getElementById(
      "email-error-message",
    ) as HTMLParagraphElement;
    const new_email = (
      document.querySelector('input[type="email"]') as HTMLInputElement
    ).value;
    axios
      .post(
        "/users/reset_email",
        {
          new_email: new_email,
        },
        {
          headers: {
            accept: "application/json",
            Authorization: "Bearer " + localStorage.getItem("access_token"),
          },
        },
      )
      .then((response) => {
        if (response.status === 200) {
          email_error_message.innerText = "Email changed successfully";
        }
      })
      .catch(() => {
        email_error_message.innerText = "Email change failed";
      });
  };

  const handleAccountDeletionSubmission = () => {
    axios
      .delete("/users/delete", {
        headers: {
          accept: "application/json",
          Authorization: "Bearer " + localStorage.getItem("access_token"),
        },
      })
      .then((response) => {
        if (response.status === 200) {
          localStorage.removeItem("access_token");
          navigate("/auth/login");
        }
      })
      .catch(() => {
        alert("Account deletion failed");
      });
  };

  return (
    <div
      className="mx-3 mb-4 mt-8 flex flex-col overflow-hidden rounded-[4px] border-2
        border-border text-text md:mx-auto md:w-[600px] lg:w-[800px] lg:flex-row
        lg:rounded-xl"
    >
      {/* Column 1 - Sidebar*/}
      {/*
      <nav className="flex w-full overflow-hidden bg-secondary text-left lg:block lg:w-max">
        <button
          type="button"
          className={`flex-1 flex-shrink-0 whitespace-nowrap p-4 text-center lg:w-full lg:text-left
            ${activeTab === "vertical-tab-1" ? "bg-primary" : ""}`}
          id="vertical-tab-1"
          aria-selected={activeTab === "vertical-tab-1"}
          data-hs-tab="#vertical-tab-1"
          aria-controls="vertical-tab-1"
          role="tab"
          onClick={() => handleTabClick("vertical-tab-1")}
        >
          Account
        </button>
        <button
          type="button"
          className={`flex-1 flex-shrink-0 whitespace-nowrap p-4 text-center lg:w-full lg:text-left
            ${activeTab === "vertical-tab-2" ? "bg-primary" : ""}`}
          id="vertical-tab-2"
          aria-selected={activeTab === "vertical-tab-2"}
          data-hs-tab="#vertical-tab-2"
          aria-controls="vertical-tab-2"
          role="tab"
          onClick={() => handleTabClick("vertical-tab-2")}
        >
          {isTabletOrMobile ? "Global Variables" : "Globals"}
        </button>
        <button
          type="button"
          className={`flex-1 flex-shrink-0 whitespace-nowrap p-4 text-center lg:w-full lg:text-left
            ${activeTab === "vertical-tab-3" ? "bg-primary" : ""}`}
          id="vertical-tab-3"
          aria-selected={activeTab === "vertical-tab-3"}
          data-hs-tab="#vertical-tab-3"
          aria-controls="vertical-tab-3"
          role="tab"
          onClick={() => handleTabClick("vertical-tab-3")}
        >
          {isTabletOrMobile ? "Account Linking" : "Linking"}
        </button>
      </nav> */}

      {/* Column 2 */}
      <div className="flex-3 w-full bg-primary px-8 py-8 sm:px-16 sm:py-10">
        {/* Main account settings content */}
        {
          <>
            <div className="mb-6">
              <h1 className="mb-3 text-2xl font-semibold sm:text-[1.75rem]">
                Account
              </h1>
              <p>Change your account information</p>
            </div>

            {/* <div className="mt-4 flex pb-4">
                  <FaUserCircle className="max-h-40 w-auto flex-shrink-0 rounded-full text-9xl" />
                  <div className="my-auto ml-4">
                    <h2 className="mb-2 text-xl">Profile Picture</h2>
                    <button
                      className="mr-4 mt-4 rounded-lg border-2 border-solid border-info p-1 px-8 text-base
                        text-info"
                    >
                      Upload
                    </button>
                    <button className="mt-2 rounded-lg border-2 border-solid border-error p-1 px-8 text-base text-error">
                      Remove
                    </button>
                  </div>
                </div> */}

            <form className="pb-4">
              <label className="mb-2 block xxl:text-lg">New Email</label>
              <input
                type="email"
                className="mb-4 w-full rounded-lg border border-border bg-secondary p-2 outline-none"
                onChange={handleEmailChangeEvents}
              />
              <button
                className="rounded-lg bg-accent p-2 px-16 text-text-contrast hover:bg-accent-hover"
                type="button"
                onClick={handleEmailChangeSubmission}
              >
                Change Email
              </button>
              <p id="email-error-message" className="text-error"></p>
            </form>

            <form className="pb-4">
              <h2 className="mb-6 mt-8 text-2xl font-semibold sm:text-[1.75rem]">
                Reset Password
              </h2>
              <label className="mb-2 block xxl:text-lg">New Password</label>
              <input
                name="password-reset-password"
                type="password"
                className="mb-4 w-full rounded-lg border border-border bg-secondary p-2 outline-none"
                onChange={handlePasswordInputEvents}
              />
              <label className="mb-2 block xxl:text-lg">
                Confirm New Password
              </label>
              <input
                name="password-reset-confirm-password"
                type="password"
                className="mb-4 w-full rounded-lg border border-border bg-secondary p-2 outline-none"
                onChange={handlePasswordInputEvents}
              />
              <p id="password-reset-error-message" className="text-error"></p>
              <button
                className="mt-4 rounded-[4px] bg-accent p-2 px-16 text-text-contrast hover:bg-accent-hover"
                type="button"
                onClick={handlePasswordResetSubmission}
              >
                Reset Password
              </button>
            </form>
            <h2 className="mb-6 mt-8 text-2xl font-semibold sm:text-[1.75rem]">
              Danger Zone
            </h2>

            <button
              className="rounded-[4px] bg-error px-5 py-2"
              type="button"
              onClick={handleAccountDeletionSubmission}
            >
              Delete my account
            </button>
          </>
        }
        {/* Global variable settings */}
        {/*}
        {activeTab === "vertical-tab-2" && (
          <>
            <h1 className="mb-4 text-3xl">Global Variables</h1>
            <p>Manage your global variables here.</p>
          </>
        )}
          */}
        {/* Account linking settings */}
        {/*
        {activeTab === "vertical-tab-3" && (
          <>
            <h1 className="mb-4 text-3xl">Account Linking</h1>
            <p>Link your account with other services.</p>
          </>
        )} */}
      </div>
    </div>
  );
};

export default Settings;
