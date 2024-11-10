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
    element: (
      <>
        <NavBar />
        <Home />
      </>
    ),
  },
  {
    path: "/auth",
    element: (
      <>
        <NavBar />
        <Auth />
      </>
    ),
  },
  {
    path: "/me",
    element: (
      <>
        <NavBar />
        <Me />
      </>
    ),
  },
  {
    path: "/settings",
    element: (
      <>
        <NavBar />
        <Settings />
      </>
    ),
  },
  {
    path: "/theme-guide",
    element: (
      <>
        <NavBar />
        <Guide />
      </>
    ),
  },
  {
    path: "/tasks",
    element: (
      <>
        <NavBar />
        <Tasks />
      </>
    ),
  },
]);

const App = () => {
  useTheme();

  return <RouterProvider router={router} />;
};

export default App;