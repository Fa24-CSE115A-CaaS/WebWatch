import { useEffect } from "react";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
// Components
import NavBar from "./components/NavBar";

// Pages
import Register from "./pages/Register";
import Login from "./pages/Login";
import Home from "./pages/Home";
import Guide from "./pages/Guide";
import Settings from "./pages/Settings";
import Tasks from "./pages/Tasks";

const router = createBrowserRouter([
  {
    path: "/",
    Component: Home,
  },
  {
    path: "/register",
    Component: Register,
  },
  {
    path: "/login",
    Component: Login,
  },
  {
    path: "/settings",
    Component: Settings,
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

  return (
    <div>
      <NavBar />
      <RouterProvider router={router}></RouterProvider>
    </div>
  );
};

export default App;
