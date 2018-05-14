# coding=utf-8

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from ihome import create_app, db

# 需求：不修改业务逻辑代码，只修改manage.py文件中的一句代码获取不同配置环境中的app
app = create_app("development")
# 创建Manager管理对象
manager = Manager(app)
Migrate(app, db)
# 添加迁移命令
manager.add_command("db", MigrateCommand)


@app.route('/', methods=['GET', 'POST'])
def index():
    # 测试redis
    # redis_store.set("name", "itcast")

    # 测试session存储
    # session["names"] = "itheima"

    return 'index'

if __name__ == "__main__":
    # app.run()
    manager.run()

