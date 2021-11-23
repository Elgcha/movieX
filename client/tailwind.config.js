module.exports = {
  purge: ['./public/**/*.html', './src/**/*.vue'],
  darkMode: 'class', // or 'media' or 'class'
  theme: {
    extend: {
      flex: {
        '3': '0 0 33.3333%',
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
      animation: ['motion-safe'],
    },
  },
  plugins: [],
}
