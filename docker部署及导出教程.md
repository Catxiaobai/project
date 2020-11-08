# docker部署及导出教程

[toc]

### 0 前后端通用命令

##### 1 docker build 通过文件夹及dockerfile构建docker镜像

如

```shell
docker build -t 镜像名称 文件夹
如切换到有代码文件夹和dockerfile的目录执行命令
docker build -t target .
```

##### 2 docker rmi 删除镜像

##### 3 docker rm -f 删除容器

#####  4 docker images 列出所有镜像

##### 5 docker save -o 路径 镜像名

##### 6 docker load -o 路径

##### 7 docker run -d -p（实际端口：容器端口）容器名

具体指令可参考

[菜鸟教程]: https://www.runoob.com/docker



### 1 前端

前端只使用了nginx依赖，因此只需要每次把dist文件重新打包即可，然后运行docker build，docker run

### 2后端

后端 每次引入了新包都要在dockerfile内添加pip install 命令重新制作