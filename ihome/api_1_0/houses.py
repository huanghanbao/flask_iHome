# coding=utf-8
# 此文件定义和房屋相关api接口
import json
from flask import current_app, jsonify
from flask import request, g
from flask import session

from ihome import constants, redis_store
from ihome import db
from ihome.models import Area, House, Facility, HouseImage
from ihome.utils.commons import login_required
from ihome.utils.image_storage import storage_image
from ihome.utils.response_code import RET
from . import api


@api.route("/house/index")
def get_house_index():
    """
    获取首页真是房屋的信息
    1.获取房屋的信息，按照房屋发布时间进行拍讯，默认真是前5个
    2.组织数据，返回应答
    """
    # 1.获取房屋的信息，按照房屋发布时间进行拍讯，默认真是前5个
    try:
        houses = House.query.order_by(House.create_time.desc()). \
            limit(constants.HOME_PAGE_MAX_HOUSES).all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="获取房屋信息失败")
    # 2.组织数据，返回应答
    house_dict_li = []
    for house in houses:
        house_dict_li.append(house.to_basic_dict())

    return jsonify(errno=RET.OK, errmsg="OK", data=house_dict_li)


@api.route("/house/<int:house_id>")
def get_house_detail(house_id):
    """
    获取房屋的详情信息:
    1.根据房屋id查询房屋的信息
    2.组织数据，返回应答
    """
    # 1.根据房屋id查询房屋的信息
    try:
        house = House.query.get(house_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="获取房屋信息失败")

    if not house:
        return jsonify(errno=RET.NODATA, errmsg="房屋不存在")

    # 2.组织数据，返回应答
    # 尝试从session获取user_id
    # 如果用户登录，获取的登录用户的id，如果用户未登录，返回-1
    user_id = session.get("user_id", -1)
    return jsonify(errno=RET.OK, errmsg="OK", data={"house": house.to_full_dict(), "user_id": user_id})


@api.route("/house/image", methods=["POST"])
@login_required
def save_house_image():
    """
    保存上传房屋图片：
    1.接收房屋id和房屋图片文件对象
    2.根据房屋id获取房屋的信息（如果获取不到，说明房屋不存在）
    3.将房屋的图片上传到七牛云
    4.创建HouseImage对象并保存房屋图片记录
    5.返回应答，上传成功
    """
    # 1.接收房屋id和房屋图片文件对象
    house_id = request.form.get("house_id")
    file = request.files.get("house_image")

    if not all([house_id, file]):
        return jsonify(errno=RET.PARAMERR, errmsg="缺少参数")

    # 2.根据房屋id获取房屋的信息（如果获取不到，说明房屋不存在）
    try:
        house = House.query.get(house_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="获取房屋信息失败")

    if not house:
        return jsonify(errno=RET.NODATA, errmsg="房屋不存在")

    # 3.将房屋的图片上传到七牛云
    try:
        key = storage_image(file.read())
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="上传房屋图片失败")

    # 4.创建HouseImage对象并保存房屋图片记录
    house_image = HouseImage()
    house_image.house_id = house_id
    house_image.url = key

    # 判断房屋是否设置了默认图片
    if not house.index_image_url:
        house.index_image_url = key

    try:
        db.session.add(house_image)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="保存房屋图片记录失败")

    # 5.返回应答，上传成功
    img_url = constants.QINIU_DOMIN_PREFIX + key
    print "img_url:", img_url
    print 'RET.OK:', RET.OK
    return jsonify(errno=RET.OK, errmsg="上传房屋图片成功", data={"img_url": img_url})


@api.route("/houses", methods=["POST"])
@login_required
def save_house_info():
    """
    保存发布房屋的信息:
    1.接收参数并进行校验
    2.创建House对象并保存房屋的基本信息
    3.将房屋的信息添加进数据库
    4.返回应答，发布房屋信息成功
    """
    # 1.接收参数并进行校验
    req_dict = request.json
    print req_dict

    title = req_dict.get('title')
    price = req_dict.get('price')
    address = req_dict.get('address')
    area_id = req_dict.get('area_id')
    room_count = req_dict.get('room_count')
    acreage = req_dict.get('acreage')
    unit = req_dict.get('unit')
    capacity = req_dict.get('capacity')
    beds = req_dict.get('beds')
    deposit = req_dict.get('deposit')
    min_days = req_dict.get('min_days')
    max_days = req_dict.get('max_days')

    if not all(
            [title, price, address, area_id, room_count, acreage, unit, capacity, beds, deposit, min_days, max_days]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数缺失')

    try:
        # 数据库中房屋单价和押金以 分 为单位保存
        price = int(float(price) * 100)
        deposit = int(float(deposit) * 100)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    # 2.创建House对象并保存房屋的基本信息
    house = House()
    house.user_id = g.user_id
    house.area_id = area_id
    house.title = title
    house.price = price
    house.address = address
    house.room_count = room_count
    house.acreage = acreage
    house.unit = unit
    house.capacity = capacity
    house.beds = beds
    house.deposit = deposit
    house.min_days = min_days
    house.max_days = max_days

    facility = req_dict.get("facility")
    if facility:
        # 获取房屋的设施信息
        try:
            facilities = Facility.query.filter(Facility.id.in_(facility)).all()
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.PARAMERR, errmsg='获取房屋信息失败')
        # 设置房屋设施信息
        house.facilities = facilities

        # 3.将房屋的信息添加进数据库
        try:
            db.session.add(house)
            db.session.commit()
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.PARAMERR, errmsg='保存房屋信息失败')

        # 4.返回应答，发布房屋信息成功
        return jsonify(errno=RET.OK, errmsg='发布房屋信息成功', data={"house_id": house.id})


@api.route("/areas")
def get_areas_info():
    """
    获取所有城区信息：
    1.获取所有城区信息
    2.组织数据，返回应答
    """
    # 先尝试从redis缓存中获取缓存的城区信息
    # 如果获取到，直接返回，如果获取不到，查询数据库
    try:
        areas_str = redis_store.get("areas")
        if areas_str:
            return jsonify(errno=RET.OK, errmsg="OK", data=json.loads(areas_str))
    except Exception as e:
        current_app.logger.error(e)

    # 1.获取所有城区信息
    try:
        areas = Area.query.all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="获取城区信息失败")

    # 2.组织数据，返回应答
    areas_dict_li = []
    for area in areas:
        areas_dict_li.append(area.to_dict())

    # 在redis中缓存城区的信息
    try:
        redis_store.set("areas", json.dumps(areas_dict_li), constants.AREA_INFO_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.error(e)

    return jsonify(errno=RET.OK, errmsg="OK", data=areas_dict_li)
