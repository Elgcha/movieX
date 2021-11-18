module.exports = {
  purge: ['./public/**/*.html', './src/**/*.vue'],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      flex: {
       '6': '0 0 16.666%',
      },
    },
    container: {
      center: true,
    },
  },
  variants: {
    extend: {
      translate: ['active', 'group-hover'],
      flex: ['hover', 'focus'],
      borderCollapse: ['hover', 'focus'],
      tableLayout: ['hover', 'focus'],
    },
  },
  plugins: [],
}
