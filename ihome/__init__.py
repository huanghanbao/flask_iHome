# coding=utf-8
import redis
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from config import config_dict

# 创建SQLAlchemy
db = SQLAlchemy()


def create_app(config_name):
    # 创建Flask应用程序实例
    app = Flask(__name__)

    # 获取配置类
    config_cls = config_dict[config_name]

    app.config.from_object(config_cls)

    # db对象进行app管理
    db.init_app(app)

    # 创建redis数据库链接对象
    redis_store = redis.StrictRedis(host=config_cls.REDIS_HOST, port=config_cls.REDIS_PORT)

    # 开启CSRF保护
    CSRFProtect(app)

    # session信息存储
    Session(app)

    return app