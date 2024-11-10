import { useEffect } from "react";

export const useTheme = () => {
  const prefersDark = window.matchMedia("(prefers-color-scheme: dark)");

  const changeTheme = () => {
    const preferTheme = prefersDark.matches ? "dark" : "light";
    const theme = localStorage.getItem("theme") || preferTheme;

    if (theme === "light") {
      localStorage.setItem("theme", "dark");
    } else {
      localStorage.setItem("theme", "light");
    }
    updateThemeClass(localStorage.getItem("theme")!);
  };

  const updateThemeClass = (theme: string) => {
    if (theme === "dark") {
      document.body.classList.add("dark");
    } else {
      document.body.classList.remove("dark");
    }
  };

  useEffect(() => {
    const onChange = (e: MediaQueryListEvent) => {
      const preferTheme = e.matches ? "dark" : "light";

      if (localStorage.getItem("theme") === null) {
        updateThemeClass(preferTheme);
      }
    };

    const preferTheme = prefersDark.matches ? "dark" : "light";
    prefersDark.addEventListener("change", onChange);
    updateThemeClass(localStorage.getItem("theme") || preferTheme);
    return () => {
      prefersDark.removeEventListener("change", onChange);
    };
  }, []);

  return { changeTheme };
};
