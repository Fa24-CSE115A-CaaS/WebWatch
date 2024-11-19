import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

const EmailAuth = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const token = urlParams.get("token");

    if (token) {
      localStorage.setItem("access_token", token);
      navigate("/settings");
    } else {
      // Handle the case where the token is missing or invalid
      navigate("/auth/login");
    }
  }, [navigate]);

  return <div>Processing...</div>;
};

export default EmailAuth;
