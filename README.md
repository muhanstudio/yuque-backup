# yuque-backup

## web界面

运行app.py，访问[http://localhost:5000](http://localhost:5000)

## 备份

修改配置文件config.yml.example为config.yml

修改配置文件config.yml中的token和book_id

backup.py

## 添加引用(适用于转移文档)

给父文档添加子文档的引用

运行refadd.py

## 文档链接本地化

将引用文档互相引用的语雀链接本地化

运行reflocal.py

## 输出小记

修改配置文件config.yml.example为config.yml

修改配置文件headers，登录后浏览器中捕捉数据

运行notes.py

## 删除导出

运行delete.py

## 资源本地化

运行filelocal.py，还在写，没写完

## 压缩导出

压缩所有的导出为一个zip文件

运行archives.py