const Settings = () => {
  return (
    <div className="w-fill min-h-screen dark:bg-gray-500 dark:text-white">
      <div className="flex">
        <div className="min-h-screen w-fit bg-slate-800 px-14 py-4 text-center">
          {/* Column 1 */}
          <div className="mb-4">
            <a>Account</a>
          </div>
          <div className="mb-4">
            <a>Variables</a>
          </div>
        </div>
        <div className="w-full">
          {/* Column 2 */}
          <div className="m-5">
            <h1 className="text-3xl">Account</h1>
            <p>Change your account information</p>
            <div className="mt-4 flex">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke-width="1.5"
                stroke="currentColor"
                className="max-h-40 w-auto rounded-full"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M17.982 18.725A7.488 7.488 0 0 0 12 15.75a7.488 7.488 0 0 0-5.982 2.975m11.963 0a9 9 0 1 0-11.963 0m11.963 0A8.966 8.966 0 0 1 12 21a8.966 8.966 0 0 1-5.982-2.275M15 9.75a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z"
                />
              </svg>
              <div className="my-auto ml-4">
                <h2 className="text-xl">Profile Picture</h2>
                <p>Change your profile picture</p>
                <button className="mr-4 mt-2 rounded-lg bg-blue-500 p-2 text-white">
                  Upload
                </button>
                <button className="mt-2 rounded-lg bg-red-500 p-2 text-white">
                  Remove
                </button>
              </div>
            </div>
            <form>
              <label>Email</label>
              <input
                type="email"
                className="w-full rounded-lg border border-gray-300 p-2"
              />
              <label>Password</label>
              <input
                type="password"
                className="w-full rounded-lg border border-gray-300 p-2"
              />
              <label>Confirm Password</label>
              <input
                type="password"
                className="w-full rounded-lg border border-gray-300 p-2"
              />
              <button className="mt-4 rounded-lg bg-blue-500 p-2 text-white">
                Submit
              </button>
              <hr className="mt-4" />
              <h2 className="mt-4 text-xl">Danger Zone</h2>
              <br />
              <button className="rounded-lg bg-red-500 p-2 text-white">
                Delete my Account
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Settings;
