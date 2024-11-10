import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

interface User {
  email: string;
}

// Allows caller to either enforce redirection to auth or not 
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
        if (redirectToAuth) navigate("/auth");
        return;
      }

      try {
        const response = await axios.get("http://localhost:8000/api/users/me", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setUser(response.data);
        setIsTokenValid(true);
      } catch (error) {
        console.error("Error fetching user data:", error);
        setIsTokenValid(false);
        if (redirectToAuth) navigate("/auth");
      }
    };

    checkTokenValidity();
  }, [navigate, redirectToAuth]);

  return { user, isTokenValid };
};

export default useAuth;