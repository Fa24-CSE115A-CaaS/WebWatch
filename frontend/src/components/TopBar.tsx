import { useState } from "react";

const NavBar = () => {
  const [show_profile_dropdown, set_show_profile_dropdown] = useState(false);
  const handleProfileDropdown = () =>
    set_show_profile_dropdown(!show_profile_dropdown);
  return (
    <nav className="bg-gray-800">
      <div className="mx-auto max-w-7xl px-2 sm:px-6 lg:px-8">
        <div className="item-center relative flex h-16 justify-between">
          <div className="absolute inset-y-0 left-0 flex items-center">
            <h1>WebWatch</h1>
          </div>
          <div className="absolute inset-y-0 right-0 flex items-center">
            <button
              className="relative flex rounded-full bg-gray-800 text-sm focus:outline-none focus:ring-2
                focus:ring-white focus:ring-offset-2 focus:ring-offset-gray-800"
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
          className="absolute right-0 z-10 mr-4 mt-4 w-56 origin-top-right rounded-md bg-white
            shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none"
          role="menu"
          aria-orientation="vertical"
          aria-labelledby="menu-button"
          tabIndex={-1}
          onMouseLeave={handleProfileDropdown}
        >
          <div className="py-1" role="none">
            <a
              href="#"
              className="block px-4 py-2 text-sm text-gray-700"
              role="menuitem"
              tabIndex={-1}
              id="menu-item-0"
            >
              Account settings
            </a>
            <form method="POST" action="#" role="none">
              <button
                type="submit"
                className="block w-full px-4 py-2 text-left text-sm text-gray-700"
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
