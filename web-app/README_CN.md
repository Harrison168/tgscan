
# 基础环境
### node
```
node v18
```
#### 使用nvm切换node 版本
```
nvm list
nvm use 18.x
```
### npm需先安装yarn包管理器
```
npm install -g yarn
```
## 开发环境部署
### 首次启动需先安装依赖包
```
yarn install
```
## 本地运行
```
yarn start test
```
## 线上编译部署
```
yarn build
yarn start production
```