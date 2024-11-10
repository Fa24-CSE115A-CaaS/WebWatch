import AuthForm from "../components/AuthForm";

interface AuthProps {
  isLogin: boolean;
}

const Auth = ({ isLogin }: AuthProps) => {
  return <AuthForm isLogin={isLogin} />;
};

export default Auth;