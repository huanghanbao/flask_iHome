# coding=utf-8
import redis
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from config import config_dict
from ihome.utils.commons import RegexConverter

# 创建SQLAlchemy
db = SQLAlchemy()

redis_store = None


def create_app(config_name):
    # 创建Flask应用程序实例
    app = Flask(__name__)

    # 获取配置类
    config_cls = config_dict[config_name]

    app.config.from_object(config_cls)

    # db对象进行app管理
    db.init_app(app)

    # 创建redis数据库链接对象
    global redis_store
    redis_store = redis.StrictRedis(host=config_cls.REDIS_HOST, port=config_cls.REDIS_PORT)

    # 开启CSRF保护
    CSRFProtect(app)

    # session信息存储
    Session(app)

    # 添加路由转换器
    app.url_map.converters['re'] = RegexConverter

    # 注册蓝图对象
    from ihome.api_1_0 import api
    app.register_blueprint(api, url_prefix="/api/v1.0")

    # 注册html静态文件的蓝图
    from ihome.web_html import html
    app.register_blueprint(html)

    return app