// tailwind.config.js
/** @type {import('tailwindcss').Config} */
module.exports = {
  corePlugins: {
    preflight: false, // disable Tailwind's reset
  },
  content: ["./src/**/*.{js,jsx,ts,tsx}", "../docs/**/*.mdx"], // my markdown stuff is in ../docs, not /src
  darkMode: ["class", '[data-theme="dark"]'], // hooks into docusaurus' dark mode settigns
  theme: {
    extend: {
      colors: {
        brand: {
          primary: "#5c6bc0",
          "primary-dark": "#4858b8",
          "primary-darker": "#4353ae",
          "primary-darkest": "#37458f",
          "primary-light": "#5665be",
          "primary-lighter": "#5c6bc0",
          "primary-lightest": "#5262bc",
        },
      },
    },
  },
  plugins: [],
};
