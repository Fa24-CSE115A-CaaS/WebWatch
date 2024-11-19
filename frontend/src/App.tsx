import { createBrowserRouter, RouterProvider } from "react-router-dom";
// Components
import NavBar from "./components/NavBar";
// Hooks
import useTheme from "./hooks/useTheme";
// Pages
import Auth from "./pages/Auth";
import Home from "./pages/Home";
import Guide from "./pages/Guide";
import Settings from "./pages/Settings";
import Tasks from "./pages/Tasks";
import EmailAuth from "./components/EmailAuth";
import Test from "./pages/Test";

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
    path: "/auth/login",
    element: (
      <>
        <NavBar />
        <Auth isLogin={true} />
      </>
    ),
  },
  {
    path: "/auth/register",
    element: (
      <>
        <NavBar />
        <Auth isLogin={false} />
      </>
    ),
  },
  {
    path: "/auth/email_auth",
    element: (
      <>
        <NavBar />
        <EmailAuth />
      </>
    ),
  },
  // Auth protected route
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
  // Auth protected route
  {
    path: "/tasks",
    element: (
      <>
        <NavBar />
        <Tasks />
      </>
    ),
  },
  {
    path: "/test",
    element: (
      <>
        <NavBar />
        <Test />
      </>
    ),
  },
]);

const App = () => {
  useTheme();

  return <RouterProvider router={router} />;
};

export default App;
