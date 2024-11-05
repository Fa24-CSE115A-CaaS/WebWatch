import { useState } from "react";
import axios from 'axios';
import { useNavigate } from "react-router-dom";

const AuthForm = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  
  const navigate = useNavigate();

  const handleLogin = async (email: string, password: string) => {
    const endpoint = "http://localhost:8000/api/users/login";
    const payload = new URLSearchParams();
    payload.append('grant_type', 'password');
    payload.append('username', email);
    payload.append('password', password);
    payload.append('scope', '');
    payload.append('client_id', 'string'); 
    payload.append('client_secret', 'string'); 
  
    try {
      const response = await axios.post(endpoint, payload, {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          "accept": "application/json",
        },
      });
  
      console.log("Success:", response.data);
      navigate('/Me');
      localStorage.setItem('access_token', response.data.access_token);
    } catch (error) {
      console.error("Error:", error);
    }
  };
  
  const handleRegister = async (email: string, password: string, confirmPassword: string) => {
    const endpoint = "http://localhost:8000/api/users/register";
    const payload = {
      email: email,
      password: password,
      confirm_password: confirmPassword
    };

    try {
      const response = await axios.post(endpoint, payload, {
        headers: {
          "Content-Type": "application/json",
          "accept": "application/json",
        },
      });
  
      console.log("Success:", response.data);
      localStorage.setItem('access_token', response.data.access_token);
      navigate('/me');
    } catch (error) {
      console.error("Error:", error);
    }
  };
  
  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (isLogin) {
      await handleLogin(email, password);
    } else {
      await handleRegister(email, password, confirmPassword);
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