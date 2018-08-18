# maoyan_spider

猫眼的几个爬虫，输出json文件

## 配置

运行前的准备，请确认已经安装好 `python` 3。

### 配置环境

```sh
# 安装 virtualenv
pip3 install virtualenv

# 新建一个虚拟环境
virtualenv --no-site-packages venv

# 引用环境
source venv/bin/activate
```

### 安装扩展包

```sh
pip install requests bs4 html5lib
```

或者

```sh
pip install -r requirements.txt
```

## 爬取

## 爬取影院

```sh
python cinemas
```

## 预览

## 预览影院

```sh
python run.py
```

打开网址 [http://127.0.0.1:5000/](http://127.0.0.1:5000/) 预览影院在地图上的效果