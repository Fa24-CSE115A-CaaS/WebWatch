import { useState } from "react";
//import useEffect from "../App";

const NavBar = () => {
  const [show_profile_dropdown, set_show_profile_dropdown] = useState(false);
  const handleProfileDropdown = () =>
    set_show_profile_dropdown(!show_profile_dropdown);
  return (
    <nav className="bg-secondary text-text">
      <div className="px-2 sm:px-6 lg:px-8">
        <div className="item-center relative flex h-16 justify-between">
          <div className="absolute inset-y-0 left-0 flex items-center">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke-width="1.5"
              stroke="currentColor"
              className="size-6"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M2.25 15a4.5 4.5 0 0 0 4.5 4.5H18a3.75 3.75 0 0 0 1.332-7.257 3 3 0 0 0-3.758-3.848 5.25 5.25 0 0 0-10.233 2.33A4.502 4.502 0 0 0 2.25 15Z"
              />
            </svg>
            &nbsp;
            <h1 className="mr-4">WebWatch</h1>
            <a className="mr-6" href="/">
              Dashboard
            </a>
          </div>
          <div className="absolute inset-y-0 right-0 flex items-center">
            <a href="/auth" className="mr-4">
              Get Started
            </a>
            <button
              className="relative flex rounded-full bg-gray-50 text-sm focus:outline-none focus:ring-2
                focus:ring-white focus:ring-offset-2 focus:ring-offset-gray-800 dark:bg-gray-800"
              id="user-menu-button"
              aria-expanded="false"
              aria-haspopup="true"
              onClick={handleProfileDropdown}
            >
              <span className="absolute -inset-1.5"></span>
              <span className="sr-only">Open user menu</span>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke-width="1.5"
                stroke="currentColor"
                className="h-8 w-8 rounded-full"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M17.982 18.725A7.488 7.488 0 0 0 12 15.75a7.488 7.488 0 0 0-5.982 2.975m11.963 0a9 9 0 1 0-11.963 0m11.963 0A8.966 8.966 0 0 1 12 21a8.966 8.966 0 0 1-5.982-2.275M15 9.75a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z"
                />
              </svg>
            </button>
          </div>
        </div>
      </div>
      {show_profile_dropdown && (
        <div
          className="text-contrast absolute right-0 z-10 mr-4 mt-4 w-fit origin-top-right rounded-md
            bg-secondary p-2 text-center shadow-lg ring-1 ring-black ring-opacity-5
            focus:outline-none"
          role="menu"
          aria-orientation="vertical"
          aria-labelledby="menu-button"
          tabIndex={-1}
          onMouseLeave={handleProfileDropdown}
        >
          <div className="" role="none">
            <a
              href="/settings"
              className="btn mb-2 block w-full bg-accent px-4 py-2 text-sm text-text-contrast
                hover:bg-accent-hover"
              role="menuitem"
              tabIndex={-1}
              id="menu-item-0"
            >
              Manage your WebWatch account
            </a>
            <a
              className="btn mb-2 block w-full bg-accent px-4 py-2 text-sm text-text-contrast
                hover:bg-accent-hover"
              href="/theme-guide"
            >
              Change Theme
            </a>
            <form method="POST" action="#" role="none">
              <button
                type="submit"
                className="btn block w-full bg-accent px-4 py-2 text-sm text-text-contrast
                  hover:bg-accent-hover"
                role="menuitem"
                tabIndex={-1}
                id="menu-item-3"
              >
                Sign out
              </button>
            </form>
          </div>
        </div>
      )}
    </nav>
  );
};

export default NavBar;
