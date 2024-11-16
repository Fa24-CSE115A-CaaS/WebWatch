// Hooks
import usePopup from "../hooks/usePopup";
import { useTheme } from "../hooks/useTheme";
import useAuth from "../hooks/useAuth";
// Icons
import { FaCircle } from "react-icons/fa";
import { IoIosCloudOutline } from "react-icons/io";

const NavBar = () => {
  const { open, setOpen, containerRef } = usePopup();
  const { changeTheme } = useTheme();
  const { user, logout } = useAuth({ redirectToAuth: false }); // Use named parameter for clarity

  return (
    <>
      <nav className="bg-secondary px-2 text-text sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between">
          <div className="flex items-center gap-4">
            <a href="/">
              <h1 className="flex items-center gap-2">
                <IoIosCloudOutline size={20} /> WebWatch
              </h1>
            </a>
          </div>
          {user && (
            <div className="flex flex-grow justify-center">
              <a href="/tasks">
                <button
                  className="w-40 rounded-lg bg-accent py-2 text-text-contrast hover:bg-accent-hover"
                  id="tasks-button"
                  aria-expanded="false"
                  aria-haspopup="true"
                >
                  Tasks
                </button>
              </a>
            </div>
          )}
          <div className="flex items-center gap-4">
            {user && (
              <button
                className="relative flex cursor-pointer rounded-full bg-gray-50 text-sm focus:outline-none
                  focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-gray-800
                  dark:bg-gray-800"
                id="user-menu-button"
                aria-expanded="false"
                aria-haspopup="true"
                onClick={() => setOpen((prev) => !prev)}
              >
                <FaCircle size={30} />
              </button>
            )}
          </div>
        </div>
      </nav>
      <div className="relative">
        {open && (
          <div
            className="absolute right-4 top-4 w-fit rounded-sm border-[1px] border-border bg-primary
              text-text"
            role="menu"
            aria-orientation="vertical"
            aria-labelledby="menu-button"
            ref={containerRef}
          >
            <a
              href="/settings"
              className="block border-b-[1px] border-border px-5 py-3"
              role="menuitem"
              tabIndex={-1}
              id="menu-item-0"
            >
              Manage Account
            </a>
            <a
              className="block border-b-[1px] border-border px-5 py-3"
              onClick={changeTheme}
            >
              Change Theme
            </a>
            <button
              className="block px-5 py-3 text-error"
              role="menuitem"
              onClick={() => {
                logout();
                setOpen(false);
              }}
            >
              Sign out
            </button>
          </div>
        )}
      </div>
    </>
  );
};

export default NavBar;
