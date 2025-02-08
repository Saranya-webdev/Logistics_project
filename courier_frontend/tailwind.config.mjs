/** @type {import('tailwindcss').Config} */
export default {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        Inria: ['Inria Sans'],
        Mono: ['Roboto Mono'],
        Condensed: ['Roboto Condensed'],
        Inter: ['Inter'],
        Roboto: ['Roboto'],
      },
            boxShadow: {
              'custom-glow': '0 0 1.5px rgba(0, 0, 0, 25%)',
            },
          },
        },
        plugins: [],
        module: {
          rules: [
            {
              test: /\.css$/i,
              use: ["style-loader", "css-loader"],
            },
          ],
        },
      };
      