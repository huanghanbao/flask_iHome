# coding=utf-8
import redis
import pymysql
pymysql.install_as_MySQLdb()


class Config(object):
    """配置类"""
    # 设置SECRET_KEY
    SECRET_KEY = 'z5nBmcVOUsZxwK6SKhx4aiLidU52GecMdO43LubPjZKhavBa+vMKrZqR3Ai+6R+2'

    # mysql数据库相关配置
    SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@192.168.105.137:3306/ihome_sz"
    # 关闭追踪数据库的修改
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # redis数据库配置
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

    # session存储配置
    # 设置session信息存放在redis数据库
    SESSION_TYPE = "redis"
    # 设置session存储到哪个redis数据库中
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    # 开启session签名
    SESSION_USE_SIGNER = True

    PERMANENT_SESSION_LIFETIME = 86400 * 2  # session 的有效期，单位是秒


class DevelopmentConfig(Config):
    """开发环境中配置类"""
    DEBUG = True


class ProductionConfig(Config):
    """生产环境中的配置类"""
    # mysql数据库相关配置
    SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@192.168.105.137:3306/ihome"


class TestingConfig(Config):
    """测试环境中的配置类"""
    # mysql数据库相关配置
    SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@192.168.105.137:3306/ihome_testcase"
    # 开启测试标志
    TESTING = True

config_dict = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig
}