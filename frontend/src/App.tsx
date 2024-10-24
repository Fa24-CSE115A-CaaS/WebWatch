import { useEffect } from "react";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
// Components
import Home from "./pages/Home";
import Guide from "./pages/Guide";

const router = createBrowserRouter([
  {
    path: "/",
    Component: Home,
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

  return <RouterProvider router={router} />;
};

export default App;
