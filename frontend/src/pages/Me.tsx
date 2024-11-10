import useAuth from "../hooks/useAuth";

const Me = () => {
  const { user } = useAuth(); // Default behavior, redirects to auth if not authenticated

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