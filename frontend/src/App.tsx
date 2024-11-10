import { createBrowserRouter, RouterProvider } from "react-router-dom";
// Components
import NavBar from "./components/NavBar";
// Hooks
import { useTheme } from "./hooks/useTheme";
// Pages
import Auth from "./pages/Auth";
import Home from "./pages/Home";
import Guide from "./pages/Guide";
import Settings from "./pages/Settings";
import Tasks from "./pages/Tasks";
import Me from "./pages/Me";

const router = createBrowserRouter([
  {
    path: "/",
    Component: Home,
  },
  {
    path: "/auth",
    Component: Auth,
  },
  {
    path: "/me",
    Component: Me,
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
  },
]);

const App = () => {
  useTheme();

  return (
    <div>
      <NavBar />
      <RouterProvider router={router}></RouterProvider>
    </div>
  );
};

export default App;
