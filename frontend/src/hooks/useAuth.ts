import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { axios } from "../config";

interface User {
  email: string;
}

// Allows caller to either enforce redirection to /auth or not
interface UseAuthOptions {
  redirectToAuth?: boolean;
}

const useAuth = ({ redirectToAuth = true }: UseAuthOptions = {}) => {
  const [user, setUser] = useState<User | null>(null);
  const [isTokenValid, setIsTokenValid] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const checkTokenValidity = async () => {
      const token = localStorage.getItem("access_token");
      if (!token) {
        setIsTokenValid(false);
        if (redirectToAuth) navigate("/auth/login");
        return;
      }

      try {
        const response = await axios.get("/users/me", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setUser(response.data);
        setIsTokenValid(true);
      } catch (error) {
        console.error("Error fetching user data:", error);
        setIsTokenValid(false);
        if (redirectToAuth) navigate("/auth/login");
      }
    };

    checkTokenValidity();
  }, [navigate, redirectToAuth]);

  const logout = () => {
    setUser(null);
    setIsTokenValid(false);
    localStorage.removeItem("access_token");
    navigate("/auth/login");
  };

  return { user, isTokenValid, logout };
};

export default useAuth;
