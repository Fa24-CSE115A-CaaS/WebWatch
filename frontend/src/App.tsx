import { useEffect } from "react";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
// Components
import Home from "./pages/Home";
import Guide from "./pages/Guide";
import Tasks from "./pages/Tasks";

const router = createBrowserRouter([
  {
    path: "/",
    Component: Home,
  },
  {
    path: "/theme-guide",
    Component: Guide,
  },
  {
    path: "/tasks",
    Component: Tasks,
  }
]);

const App = () => {
  useEffect(() => {
    const theme = localStorage.getItem("theme");
    if (theme === "dark") {
      document.body.classList.add("dark");
    }
  }, []);

  return <RouterProvider router={router} />;
};

export default App;
