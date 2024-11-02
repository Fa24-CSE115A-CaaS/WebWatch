import { useState } from "react";

const AuthForm = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  interface AuthFormProps {
    email: string;
    password: string;
    confirmPassword?: string;
  }

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const endpoint = isLogin ? "/api/login" : "/api/register";
    const payload: AuthFormProps = { email, password, ...(isLogin ? {} : { confirmPassword }) };

    try {
      const response = await fetch(endpoint, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const data = await response.json();
      console.log("Success:", data);
      // Handle successful response (e.g., redirect, show message)
    } catch (error) {
      console.error("Error:", error);
      // Handle error (e.g., show error message)
    }
  };

  return (
    <div className="w-1/3 mx-auto mt-8 rounded min-h-screen text-text">
      <div className="flex justify-center mb-4">
        <div className="w-full rounded-xl border-solid border-border border-2 bg-primary">
          <div className="m-5">
            <div className="flex justify-center m-4">
              <button
                className={`relative px-4 py-2 font-bold mx-4 text-lg ${isLogin ? "decoration-accent" : ""}`}
                onClick={() => setIsLogin(true)}
              >
                Login
                {isLogin && (
                  <span className="absolute left-0 right-0 bottom-0 h-0.5 bg-accent transform -translate-y-1/2"></span>
                )}
              </button>
              <button
                className={`relative px-4 py-2 font-bold mx-4 text-lg ${!isLogin ? "decoration-accent" : ""}`}
                onClick={() => setIsLogin(false)}
              >
                Register
                {!isLogin && (
                  <span className="absolute left-0 right-0 bottom-0 h-0.5 bg-accent transform -translate-y-1/2"></span>
                )}
              </button>
            </div>
            <form onSubmit={handleSubmit}>
              <div className="mb-4">
                <label htmlFor="email" className="block mb-2">Email</label>
                <input
                  type="email"
                  id="email"
                  className="w-full rounded-lg border border-border bg-secondary p-2"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
              </div>
              <div className="mb-4">
                <label htmlFor="password" className="block mb-2">Password</label>
                <input
                  type="password"
                  id="password"
                  className="w-full rounded-lg border border-border bg-secondary p-2"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
              </div>
              {!isLogin && (
                <div className="mb-4">
                  <label htmlFor="confirm-password" className="block mb-2">Confirm Password</label>
                  <input
                    type="password"
                    id="confirm-password"
                    className="w-full rounded-lg border border-border bg-secondary p-2"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                  />
                </div>
              )}
              <button type="submit" className="mt-4 w-full rounded-lg bg-accent p-2 text-text-contrast hover:bg-accent-hover">
                {isLogin ? "Login" : "Create Account"}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AuthForm;