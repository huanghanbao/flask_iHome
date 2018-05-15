# coding=utf-8
# 此蓝图用户给浏览器提供静态页面
from flask import Blueprint
from flask import current_app

html = Blueprint("html", __name__)

# 当浏览器访问一个网站的时候，浏览器会自动范文网站下的一个文件favicon.ico,为了获取网站的图标
# http://127.0.0.1:5000/favicon.ico


@html.route('/<re(".*"):file_name>')
def get_static_html(file_name):
    # 获取静态文件目录下对应的静态文件的内容并返回给浏览器
    if file_name == '':
        # 说明用户访问的是根路径默认返回index.html
        file_name = 'index.html'

    if file_name != "favicon.ico":
        file_name = "html/" + file_name

    return current_app.send_static_file(file_name)
    # return current_app.send_static_file('html/index.html')
