/* webpack.config.js
 * @ Cong Min
 */
// run `npm install webpack extract-text-webpack-plugin html-webpack-plugin --save-dev` before
var webpack = require('webpack'),
    ExtractTextPlugin = require('extract-text-webpack-plugin'),
    HtmlPlugin = require('html-webpack-plugin');

module.exports = {
    entry: {
        // 输入
        app: ['./src/js/app'],
        // 第三方库modules单独打包, 填入modules名即可
        lib: ['./src/js/jquery.min', './src/js/tagcloud.min'],
        // result
        res: ['./src/js/res'],
        resLib: ['./src/js/jquery.min', './src/js/stopExecutionOnTimeout']
    },
    output: {
        // 输出
        path: './dist/',
        filename: 'js/[name].js?[chunkhash:8]',
        publicPath: "/frontend/dist/"
    },
    plugins: [
        // 第三方库modules单独打包
        new webpack.optimize.CommonsChunkPlugin({
            name: "lib",
            filename: "js/lib.js?[chunkhash:8]",
            chunks: ["app", "lib"]
        }),
        // 输出index.html
        new HtmlPlugin({
            // html模板文件地址
            template: './src/index.html',
            // 输出路径及文件名
            filename: './index.html',
            // chunks表示要引用entry里面的入口
            chunks: ['app', 'lib'],
            // script插入的标签
            inject: 'body'
        }),
        // 输出result.html
        new HtmlPlugin({
            template: './src/result.html',
            filename: './result.html',
            chunks: ['res', 'resLib'],
            inject: 'body'
        }),
        // 输出css (link标签方式插入)
        new ExtractTextPlugin('css/[name].css?[contenthash:8]'),
        // 配置生产环境
        new webpack.DefinePlugin({
            'process.env': {
                NODE_ENV: '"production"'
            }
        }),
        new webpack.optimize.UglifyJsPlugin({
            compress: {
                warnings: false
            }
        })
    ],
    module: {
        loaders: [{
            // 处理html, 如img-src
            // run `npm install html-loader --save-dev` before
            test: /\.html$/, loader: 'html'
        },  {
            // run `npm install style-loader css-loader --save-dev` before
            test: /\.css$/, loader: ExtractTextPlugin.extract(['css'])
        },  {
            // 压缩图片, <=8k的将编译为base64
            // run `npm install url-loader image-webpack-loader --save-dev` before
            test: /\.(png|jpg|gif)$/, loaders: [ 'url?limit=8192&name=img/[name].[ext]?[hash:8]', 'image-webpack' ]
        },  {
            // 字体
            // run `npm install url-loader --save-dev` before
            test: /\.(eot|woff|woff2|ttf|svg)/, loader: 'url', query: { limit: 10240, prefix: 'font/', name: 'font/[name].[ext]?[hash:8]' }
        },  {
            // JSON
            // run `npm install json-loader --save-dev` before
            test: /\.json$/, loader: 'json'
        }],
        resolve: {
            extensions: ['', '.js', '.json']
            // require('./main') <=> require('./res.js')
        }
    }
};