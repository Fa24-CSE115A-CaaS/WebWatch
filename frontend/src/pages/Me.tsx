import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const Me = () => {
  interface User {
    email: string;
  }

  const [user, setUser] = useState<User | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchUserData = async () => {
      const token = localStorage.getItem("access_token");
      if (!token) {
        navigate("/auth");
        return;
      }

      try {
        const response = await axios.get("http://localhost:8000/api/users/me", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setUser(response.data);
      } catch (error) {
        console.error("Error fetching user data:", error);
        navigate("/auth");
      }
    };

    fetchUserData();
  }, [navigate]);

  if (!user) {
    return <div>Loading...</div>;
  }

  return (
    <div
      className="font-font flex min-h-screen flex-col items-center justify-start bg-primary p-4
        text-center text-white"
    >
      <header className="mb-8 mt-16">
        <h1 className="mb-4 text-5xl font-bold text-accent">
          Welcome, {user.email}{" "}
        </h1>
      </header>
    </div>
  );
};

export default Me;
