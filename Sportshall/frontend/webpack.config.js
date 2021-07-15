const path = require("path");
const webpack = require("webpack");

module.exports = {
  entry: "./src/index.js",
  output: {
    path: path.resolve(__dirname, "./static/frontend"),
    filename: "[name].js",
    sourceMapFilename: "[name].js.map",
  },
  devtool: "source-map",
  watch: true,
  module: {
    rules: [
      {
        test: /\.css$/,
        use: {
          loader: "style-loader", 
          loader: "css-loader",
        },
      },
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader"
        },
      },
    ],
  },
  optimization: {
    minimize: true,
  },
  watchOptions: {
    poll: 5000,
    ignored: /node_modules/,
  },
  plugins: [
    new webpack.DefinePlugin({
      "process.env": {
        // This has effect on the react lib size
        NODE_ENV: JSON.stringify("development"),
      },
    }),
  ],
};
