# daka_RasPi
记录一次嵌入式系统的课程设计，在树莓派4上使用摄像头和GY-906(MLX90614)模块，搭成简易的带体温检测与人脸识别的非接触式打卡系统。

两个文件夹：
- client 客户端（python），运行于树莓派上
  - main.py 主程序，管控整个流程
  - libFace.py 人脸处理函数
  - libSQL.py 数据库相关函数
  - MLX90614.py 模块的操作函数
- server 服务端（php+mysql），运行于服务器上
  - faces 存放人脸图片
  - api.php 客户端接口api
  - daka.sql 数据库结构
  - index.html 用户管理后台
  - log.html 日志查看面板
