const Register = () => {
  return (
    <div className="w-1/3 mx-auto mt-8 rounded min-h-screen text-text">
      <div className="flex">
        <div className="w-full rounded-xl border-solid border-border border-2 bg-primary">
          <div className="m-5">
            <h1 className="text-3xl">Register</h1>
            <form>
              <label>Email</label>
              <input
                type="email"
                className="w-full rounded-lg border border-border bg-secondary p-2"
              />
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
                Create Account
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Register;
