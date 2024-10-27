import { useEffect } from "react";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
// Components
import NavBar from "./components/NavBar";

// Pages
import Home from "./pages/Home";
import Guide from "./pages/Guide";
import Settings from "./pages/Settings";

const router = createBrowserRouter([
  {
    path: "/",
    Component: Home,
  },
  {
    path: "/settings",
    Component: Settings,
  },
  {
    path: "/theme-guide",
    Component: Guide,
  },
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
