# coding=utf-8
from . import api
import logging
from ihome import redis_store
from flask import current_app


# 使用蓝图对象注册路由
@api.route('/', methods=['GET', 'POST'])
def index():
    # 测试redis
    # redis_store.set("name", "itcast")

    # 测试session存储
    # session["names"] = "itheima"

    # 测试日志功能
    # logging.fatal("重大的，危险的")
    # logging.error("错误")
    # logging.warn("警告")
    # logging.info("信息")
    # logging.debug("调试")

    # current_app.logger.fatal("重大的，危险的")
    # current_app.logger.error("错误")
    # current_app.logger.warn("警告")
    # current_app.logger.info("信息")
    # current_app.logger.debug("调试")

    return 'index'