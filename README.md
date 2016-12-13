# LeanEngine Python APM Client

[LeanEngine APM](https://apm.leanapp.cn) Python Client。

## 使用

### 安装依赖

在 Python 云引擎项目的 requirements.txt 中增加一行：

```
git+https://github.com/aisk/leanengine-python-apm.git@master#egg=leanengine-apm
```

部署到云引擎即可自动安装 `leanengine-python-apm`。本地开发可使用 `$ pip install -Ur requirements.txt` 来安装依赖。

> **注意**：目前 `leanengine-python-apm` 依赖 `leancloud-sdk` 版本 > 1.9.0。

### 初始化

登录 https://apm.leanapp.cn ，使用 LeanCloud 账号登录，点击需要使用的应用名，即可获取到 APM 需要的 token。

在 `wsgi.py` 文件中，添加如下代码：

```python
import apm

apm.init('your-leanengine-apm-token')
```

> **注意**：`your-leanengine-apm-token` 请替换成对应应用的 token。

### 启用 LeanCloud 数据存储性能统计

在 `wsgi.py` 文件中添加如下代码：

```python
apm.storage.install()
```

### 启用 WebHosting 性能统计

#### Flask

开启 Flask WebHosting 性能统计，只需要在项目的 `flask.Flask` 实例上安装 `apm.FlaskMiddleware` 这个 [WSGI middleware](https://www.python.org/dev/peps/pep-0333/#middleware-components-that-play-both-sides) 就可以了。

```python
import flask
import apm

app = flask.Flask(__name__)

@app.rooute('/')
def index():
    return 'hello'

# 以及所有 flask 相关的代码

app = apm.FlaskMiddleware(flask)
```

> **注意**：请确保 apm.FlaskMiddeware 是 flask.Flask 实例上安装的第一个 WSGI middleware。

如果是使用命令行工具创建的 Python Flask 项目，只需要将 `cloud.py` 中的

```python
engine = Engine(app)
```

改成

```python
engine = Engine(apm.FlaskMiddleware(app))
```

即可。
