/** @type {import('tailwindcss').Config} */
export default {
<<<<<<< HEAD
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
=======
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
>>>>>>> origin/main
  theme: {
    extend: {
      fontFamily: {
        Inria: ['Inria Sans'],
        Mono: ['Roboto Mono'],
        Condensed: ['Roboto Condensed'],
        Inter: ['Inter'],
        Roboto: ['Roboto'],
<<<<<<< HEAD
    },
    },
  },
  plugins: [],
};
=======
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
      
>>>>>>> origin/main
