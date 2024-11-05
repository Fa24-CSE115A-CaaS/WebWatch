const Settings = () => {
  return (
    <div className="w-2/3 mx-auto mt-8 rounded min-h-screen text-text">
      <div className="flex">
        <div className="rounded-l-xl border-solid border-border border-2 min-h-screen w-1/3 min-w-fit bg-secondary text-left">
          {/* Column 1 */}
          <div className="rounded-tl-xl p-4 w-full bg-primary">
            <a>Account</a>
          </div>
          <div className="p-4 w-full">
            <a>Global Variables</a>
          </div>
        </div>
        <div className="w-full rounded-r-xl border-solid border-border border-y-2 border-r-2 bg-primary">
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
                <button className="mr-4 mt-4 px-8 rounded-lg border-info border-solid border-2 text-info p-1">
                  Upload
                </button>
                <button className="mt-2 px-8 rounded-lg border-error border-solid border-2 text-error p-1">Remove</button>
              </div>
            </div>
            <form>
              <label>Email</label>
              <input
                type="email"
                className="w-full rounded-lg border border-border bg-secondary p-2"
              />
              <h2 className="text-2xl my-8">Reset Password</h2>
              <label>Password</label>
              <input
                type="password"
                className="w-full rounded-lg border border-border bg-secondary p-2"
              />
              <label>Confirm Password</label>
              <input
                type="password"
                className="w-full rounded-lg border border-border bg-secondary p-2"
              />
              <button className="mt-4 rounded-lg bg-accent p-2 px-16 text-text-contrast hover:bg-accent-hover">
                Save
              </button>
            </form>
            <h2 className="text-xl font-bold mt-8 mb-4">Danger Zone</h2>
            <button className="rounded-lg bg-error p-2">
              Delete my account
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Settings;
