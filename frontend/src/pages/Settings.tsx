import { useState } from "react";
import { FaUserCircle } from "react-icons/fa";

const Settings = () => {
  const [activeTab, setActiveTab] = useState("vertical-tab-1");

  const handleTabClick = (tabId: string) => {
    setActiveTab(tabId);
  };

  return (
    <div className="mx-auto mt-8 min-h-screen w-1/2 rounded text-text">
      <div className="flex">
        {/* Column 1 - Sidebar*/}
        <nav
          className="min-h-screen w-max overflow-hidden rounded-l-xl border-2 border-solid
            border-border bg-secondary text-left"
        >
          <div
            className="rounded-tl-xl"
            aria-label="Tabs"
            role="tablist"
            aria-orientation="vertical"
          >
            <button
              type="button"
              className={`w-full whitespace-nowrap p-4 text-left
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
              className={`w-full whitespace-nowrap p-4 text-left
                ${activeTab === "vertical-tab-2" ? "bg-primary" : ""}`}
              id="vertical-tab-2"
              aria-selected={activeTab === "vertical-tab-2"}
              data-hs-tab="#vertical-tab-2"
              aria-controls="vertical-tab-2"
              role="tab"
              onClick={() => handleTabClick("vertical-tab-2")}
            >
              Global Variables
            </button>
            <button
              type="button"
              className={`w-full whitespace-nowrap p-4 text-left
                ${activeTab === "vertical-tab-3" ? "bg-primary" : ""}`}
              id="vertical-tab-3"
              aria-selected={activeTab === "vertical-tab-3"}
              data-hs-tab="#vertical-tab-3"
              aria-controls="vertical-tab-3"
              role="tab"
              onClick={() => handleTabClick("vertical-tab-3")}
            >
              Account Linking
            </button>
          </div>
        </nav>

        {/* Column 2 */}
        <div className="w-full rounded-r-xl border-y-2 border-r-2 border-solid border-border bg-primary">
          <div className="m-5 px-10 py-6">
            {/* Main account settings content */}
            {activeTab === "vertical-tab-1" && (
              <>
                <h1 className="mb-4 text-3xl">Account</h1>
                <p className="mb-4">Change your account information</p>
                <div className="mt-4 flex pb-4">
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
                </div>
                <form className="pb-4">
                  <label className="mb-2 block text-lg">Email</label>
                  <input
                    type="email"
                    className="mb-4 w-full rounded-lg border border-border bg-secondary p-2 outline-none"
                  />
                  <h2 className="my-8 mb-4 text-2xl">Reset Password</h2>
                  <label className="mb-2 block text-lg">Password</label>
                  <input
                    type="password"
                    className="mb-4 w-full rounded-lg border border-border bg-secondary p-2 outline-none"
                  />
                  <label className="mb-2 block text-lg">Confirm Password</label>
                  <input
                    type="password"
                    className="mb-4 w-full rounded-lg border border-border bg-secondary p-2 outline-none"
                  />
                  <button className="mt-4 rounded-lg bg-accent p-2 px-16 text-text-contrast hover:bg-accent-hover">
                    Save
                  </button>
                </form>
                <h2 className="my-8 mb-4 text-2xl">Danger Zone</h2>
                <button className="rounded-lg bg-error px-3 py-2">
                  Delete my account
                </button>
              </>
            )}
            {/* Global variable settings */}
            {activeTab === "vertical-tab-2" && (
              <>
                <h1 className="mb-4 text-3xl">Global Variables</h1>
                <p>Manage your global variables here.</p>
              </>
            )}
            {/* Account linking settings */}
            {activeTab === "vertical-tab-3" && (
              <>
                <h1 className="mb-4 text-3xl">Account Linking</h1>
                <p>Link your account with other services.</p>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Settings;
