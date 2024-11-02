import { useState } from 'react';
import { FaUserCircle } from 'react-icons/fa';

const Settings = () => {
  const [activeTab, setActiveTab] = useState('vertical-tab-1');

  const handleTabClick = (tabId: string) => {
    setActiveTab(tabId);
  };

  const handleAccountUpdate = () => {
    // Set Email to a new value
    let newEmail = document.getElementsByName('newEmail')[0].textContent;
    let newPassword = document.getElementsByName('password')[0].textContent;
    let confirmPassword = document.getElementsByName('confirmPassword')[0].textContent;
    // Check if the passwords match
    if (newPassword !== confirmPassword) {
      alert('Passwords do not match');
      return;
    }
    let uid = localStorage.getItem('uid');
    // Update the user's email
    fetch("/api/users/" + uid, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email: newEmail,
        password: newPassword,
        id: uid,
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          alert('Account details updated successfully');
        } else {
          alert('Account update failed');
        }
      });
  };

  return (
    <div className="w-1/2 mx-auto mt-8 rounded min-h-screen text-text">
      <div className="flex">
        {/* Column 1 - Sidebar*/}
        <nav className="rounded-l-xl border-solid border-border border-2 min-h-screen w-max bg-secondary text-left">
          <div className="rounded-tl-xl" aria-label="Tabs" role="tablist" aria-orientation="vertical">
            <button
              type="button"
              className={`w-full p-4 text-left whitespace-nowrap ${activeTab === 'vertical-tab-1' ? 'bg-primary' : ''}`}
              id="vertical-tab-1"
              aria-selected={activeTab === 'vertical-tab-1'}
              data-hs-tab="#vertical-tab-1"
              aria-controls="vertical-tab-1"
              role="tab"
              onClick={() => handleTabClick('vertical-tab-1')}
            >
              Account
            </button>
            <button
              type="button"
              className={`w-full p-4 text-left whitespace-nowrap ${activeTab === 'vertical-tab-2' ? 'bg-primary' : ''}`}
              id="vertical-tab-2"
              aria-selected={activeTab === 'vertical-tab-2'}
              data-hs-tab="#vertical-tab-2"
              aria-controls="vertical-tab-2"
              role="tab"
              onClick={() => handleTabClick('vertical-tab-2')}
            >
              Global Variables
            </button>
            <button
              type="button"
              className={`w-full p-4 text-left whitespace-nowrap ${activeTab === 'vertical-tab-3' ? 'bg-primary' : ''}`}
              id="vertical-tab-3"
              aria-selected={activeTab === 'vertical-tab-3'}
              data-hs-tab="#vertical-tab-3"
              aria-controls="vertical-tab-3"
              role="tab"
              onClick={() => handleTabClick('vertical-tab-3')}
            >
              Account Linking
            </button>
          </div>
        </nav>

        {/* Column 2 */}
        <div className="w-full rounded-r-xl border-solid border-border border-y-2 border-r-2 bg-primary">
          <div className="m-5 px-10 py-6">
            {/* Main account settings content */}
            {activeTab === 'vertical-tab-1' && (
              <>
                <h1 className="text-3xl mb-4">Account</h1>
                <p className="mb-4">Change your account information</p>
                <div className="mt-4 flex pb-4">
                  <FaUserCircle className="max-h-40 w-auto rounded-full text-9xl flex-shrink-0" />
                  <div className="my-auto ml-4">
                    <h2 className="text-xl mb-2">Profile Picture</h2>
                    <button className="mr-4 mt-4 px-8 rounded-lg border-info border-solid border-2 text-info p-1 text-base">
                      Upload
                    </button>
                    <button className="mt-2 px-8 rounded-lg border-error border-solid border-2 text-error p-1 text-base">
                      Remove
                    </button>
                  </div>
                </div>
                <form className="pb-4">
                  <label className="text-lg mb-2 block">Email</label>
                  <input
                    name="newEmail"
                    type="email"
                    className="w-full rounded-lg border border-border bg-secondary p-2 outline-none mb-4"
                  />
                  <h2 className="text-2xl my-8 mb-4">Reset Password</h2>
                  <label className="text-lg mb-2 block">Password</label>
                  <input
                    name="password"
                    type="password"
                    className="w-full rounded-lg border border-border bg-secondary p-2 outline-none mb-4"
                  />
                  <label className="text-lg mb-2 block">Confirm Password</label>
                  <input
                    name="confirmPassword"
                    type="password"
                    className="w-full rounded-lg border border-border bg-secondary p-2 outline-none mb-4"
                  />
                  <button className="mt-4 rounded-lg bg-accent p-2 px-16 text-text-contrast hover:bg-accent-hover" onClick={
                    () => handleAccountUpdate()
                  }>
                    Save
                  </button>
                </form>
                <h2 className="text-2xl my-8 mb-4">Danger Zone</h2>
                <button className="rounded-lg bg-error px-3 py-2">
                  Delete my account
                </button>
              </>
            )}
            {/* Global variable settings */}
            {activeTab === 'vertical-tab-2' && (
              <>
                <h1 className="text-3xl mb-4">Global Variables</h1>
                <p>Manage your global variables here.</p>
              </>
            )}
            {/* Account linking settings */}
            {activeTab === 'vertical-tab-3' && (
              <>
                <h1 className="text-3xl mb-4">Account Linking</h1>
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
