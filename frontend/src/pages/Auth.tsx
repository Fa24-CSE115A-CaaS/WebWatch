import { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const AuthForm = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const navigate = useNavigate();

  useEffect(() => {
    const hash = window.location.hash;
    setIsLogin(hash !== "#register");
  }, []);

  const handleLogin = async (email: string, password: string) => {
    const endpoint = "http://localhost:8000/api/users/login";
    const payload = new URLSearchParams();
    payload.append("grant_type", "password");
    payload.append("username", email);
    payload.append("password", password);
    payload.append("scope", "");
    payload.append("client_id", "");
    payload.append("client_secret", "");

    try {
      const response = await axios.post(endpoint, payload, {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          accept: "application/json",
        },
      });

      console.log("Success:", response.data);
      navigate("/Me");
      localStorage.setItem("access_token", response.data.access_token);
    } catch (error) {
      console.error("Error:", error);
      setError("Login failed. Please check your credentials.");
    } finally {
      setLoading(false);
    }
  };

  const handleRegister = async (
    email: string,
    password: string,
    confirmPassword: string,
  ) => {
    const endpoint = "http://localhost:8000/api/users/register";
    const payload = {
      email: email,
      password: password,
      confirm_password: confirmPassword,
    };

    try {
      const response = await axios.post(endpoint, payload, {
        headers: {
          "Content-Type": "application/json",
          accept: "application/json",
        },
      });

      console.log("Success:", response.data);
      localStorage.setItem("access_token", response.data.access_token);
      navigate("/me");
    } catch (error) {
      console.error("Error:", error);
      setError("Registration failed. Please try again.");
    } finally {
      setLoading(false);
    }
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
              >
                Login
                {isLogin && (
                  <span className="absolute bottom-0 left-0 right-0 h-0.5 -translate-y-1/2 transform bg-accent"></span>
                )}
              </button>
              <button
                className={`relative mx-4 px-4 py-2 text-lg font-bold ${!isLogin ? "decoration-accent" : ""}`}
                onClick={() => handleTabSwitch(false)}
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
                  />
                </div>
              )}
              <button
                type="submit"
                className="mt-4 w-full rounded-lg bg-accent p-2 text-text-contrast hover:bg-accent-hover"
                disabled={loading}
              >
                {loading ? "Processing..." : isLogin ? "Login" : "Create Account"}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AuthForm;