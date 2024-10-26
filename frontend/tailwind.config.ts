import type { Config } from "tailwindcss";

export default {
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      screens: {
        xxl: "1600px",
      },
      fontFamily: {
        main: ["Space Grotesk", "Roboto", "sans-serif"],
      },
      colors: {
        background: "var(--background)",
        primary: "var(--primary)",
        secondary: "var(--secondary)",
        accent: "var(--accent)",
        "accent-hover": "var(--accent-hover)",
        border: "var(--border)",
        error: "var(--error)",
        info: "var(--info)",
        text: "var(--text)",
        "text-contrast": "var(--text-contrast)",
      },
    },
  },
  plugins: [],
} satisfies Config;
