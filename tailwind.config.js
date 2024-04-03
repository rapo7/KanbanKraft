module.exports = {
  content: ["./**/*.py", "./*/templates/**/*.html", "./templates/**/*.html"],
  theme: {
    fontFamily: {
      sans: ["InterVariable", "sans-serif"],
    }
  },
  plugins: [require('@tailwindcss/forms')],
}
