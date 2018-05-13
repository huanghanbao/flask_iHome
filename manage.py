# coding=utf-8
from flask import Flask


class Config(object):
    """配置类"""
    DEBUG = True


# 创建Flask应用程序实例
app = Flask(__name__)

app.config.from_object(Config)


@app.route('/')
def index():
    return 'index'


if __name__ == "__main__":
    app.run()