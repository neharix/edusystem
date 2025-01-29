/** @type {import('tailwindcss').Config} */
export default {
  content: ["./src/**/*.{html,vue,js}", "./index.html", "./node_modules/flowbite/**/*.js"],
  theme: {
    extend: {},
  },
  plugins: [
    require('flowbite/plugin')
  ],
};
