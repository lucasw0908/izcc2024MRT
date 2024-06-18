const path = require('path');
module.exports = {
  entry: './app/static/js/index.ts',
  output: {
    filename: 'index.bundle.js',
    path: path.resolve(__dirname, './app/static/js/dist')
  }
};