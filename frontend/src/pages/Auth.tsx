import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import AuthForm from "../components/AuthForm";
import useAuth from "../hooks/useAuth";

interface AuthProps {
  isLogin: boolean;
}

const Auth = ({ isLogin }: AuthProps) => {
  const { isTokenValid } = useAuth({ redirectToAuth: false });
  const navigate = useNavigate();

  useEffect(() => {
    if (isTokenValid) {
      navigate("/tasks");
    } else {
      localStorage.removeItem("access_token");
    }
  }, [isTokenValid, navigate]);

  if (isTokenValid) {
    return <div>Loading...</div>;
  }

  return <AuthForm isLogin={isLogin} />;
};

export default Auth;