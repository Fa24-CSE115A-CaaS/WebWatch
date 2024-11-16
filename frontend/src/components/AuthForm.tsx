import { useState } from "react";
import { axios } from "../config";
import { useNavigate } from "react-router-dom";
import { AxiosError } from "axios";

interface AuthFormProps {
  isLogin: boolean;
}

const AuthForm = ({ isLogin: initialIsLogin }: AuthFormProps) => {
  const [isLogin, setIsLogin] = useState(initialIsLogin);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const navigate = useNavigate();

  const handleLogin = async (email: string, password: string) => {
    const payload = new URLSearchParams();
    payload.append("grant_type", "password");
    payload.append("username", email);
    payload.append("password", password);
    payload.append("scope", "");
    payload.append("client_id", "");
    payload.append("client_secret", "");

    try {
      setLoading(true);
      const response = await axios.post("/users/login", payload, {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          accept: "application/json",
        },
      });

      localStorage.setItem("access_token", response.data.access_token);
      navigate("/tasks");
    } catch (error) {
      handleError(error, "Login failed. Please check your credentials.");
    } finally {
      setLoading(false);
    }
  };

  const handleRegister = async (
    email: string,
    password: string,
    confirmPassword: string,
  ) => {
    const payload = {
      email: email,
      password: password,
      confirm_password: confirmPassword,
    };

    try {
      setLoading(true);
      const response = await axios.post("/users/register", payload);
      localStorage.setItem("access_token", response.data.access_token);
      navigate("/tasks");
    } catch (error) {
      handleError(error, "Registration failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleLoginLink = async (email: string) => {
    try {
      setLoading(true);
      await axios.post(
        "/users/email_auth",
        { email },
        {
          headers: {
            "accept": "application/json",
            "Content-Type": "application/json",
          },
        }
      );
      setError("A login link has been sent to your email.");
    } catch (error) {
      handleError(error, "Failed to send login link. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleError = (error: unknown, defaultMessage: string) => {
    const axiosError = error as AxiosError;
    if (axiosError.response) {
      const errorDetails = (
        axiosError.response.data as { detail: { msg: string }[] }
      ).detail;
      if (Array.isArray(errorDetails)) {
        const errorMessages = errorDetails
          .map((err: { msg: string }) => err.msg)
          .filter((msg: string | undefined) => msg)
          .join(", ");
        setError(`Error: ${errorMessages}`);
      } else {
        setError(defaultMessage);
      }
    } else {
      setError("An unexpected error occurred. Please try again.");
    }
    console.error("Error:", axiosError);
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    if (!email || !password || (!isLogin && password !== confirmPassword)) {
      setError("Please fill in all fields correctly.");
      setLoading(false);
      return;
    }

    if (isLogin) {
      await handleLogin(email, password);
    } else {
      await handleRegister(email, password, confirmPassword);
    }
  };

  const handleTabSwitch = (isLogin: boolean) => {
    setIsLogin(isLogin);
    setError("");
    setLoading(false);
    navigate(isLogin ? "/auth/login" : "/auth/register");
  };

  return (
    <div className="mx-auto mt-8 min-h-screen w-1/3 rounded text-text">
      <div className="mb-4 flex justify-center">
        <div className="w-full rounded-xl border-2 border-solid border-border bg-primary">
          <div className="m-5">
            <div className="m-4 flex justify-center">
              <button
                className={`relative mx-4 px-4 py-2 text-lg font-bold ${isLogin ? "decoration-accent" : ""}`}
                onClick={() => handleTabSwitch(true)}
                disabled={loading}
              >
                Login
                {isLogin && (
                  <span className="absolute bottom-0 left-0 right-0 h-0.5 -translate-y-1/2 transform bg-accent"></span>
                )}
              </button>
              <button
                className={`relative mx-4 px-4 py-2 text-lg font-bold ${!isLogin ? "decoration-accent" : ""}`}
                onClick={() => handleTabSwitch(false)}
                disabled={loading}
              >
                Register
                {!isLogin && (
                  <span className="absolute bottom-0 left-0 right-0 h-0.5 -translate-y-1/2 transform bg-accent"></span>
                )}
              </button>
            </div>
            <form onSubmit={handleSubmit}>
              {error && <div className="mb-4 text-red-500">{error}</div>}
              <div className="mb-4">
                <label htmlFor="email" className="mb-2 block">
                  Email
                </label>
                <input
                  type="email"
                  id="email"
                  className="w-full rounded-lg border border-border bg-secondary p-2"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  disabled={loading}
                />
              </div>
              <div className="mb-4">
                <label htmlFor="password" className="mb-2 block">
                  Password
                </label>
                <input
                  type="password"
                  id="password"
                  className="w-full rounded-lg border border-border bg-secondary p-2"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  disabled={loading}
                />
              </div>
              {!isLogin && (
                <div className="mb-4">
                  <label htmlFor="confirm-password" className="mb-2 block">
                    Confirm Password
                  </label>
                  <input
                    type="password"
                    id="confirm-password"
                    className="w-full rounded-lg border border-border bg-secondary p-2"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    disabled={loading}
                  />
                </div>
              )}
              <button
                type="submit"
                className="mt-4 w-full rounded-lg bg-accent p-2 text-text-contrast hover:bg-accent-hover"
                disabled={loading}
              >
                {loading
                  ? "Processing..."
                  : isLogin
                    ? "Login"
                    : "Create Account"}
              </button>
              {isLogin && (
                <>
                  <div className="my-4 flex items-center">
                    <hr className="flex-grow border-t border-border" />
                    <span className="mx-4 text-gray-500">or</span>
                    <hr className="flex-grow border-t border-border" />
                  </div>
                  <button
                    type="button"
                    className="w-full rounded-lg bg-accent p-2 text-text-contrast hover:bg-secondary-hover"
                    onClick={() => handleLoginLink(email)}
                    disabled={loading}
                  >
                    Send login link to email
                  </button>
                </>
              )}
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AuthForm;