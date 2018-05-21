function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function () {
    // $('.popup_con').fadeIn('fast');
    // $('.popup_con').fadeOut('fast');

    // TODO: 在页面加载完毕之后获取区域信息
    $.get("api/v1.0/areas", function (resp) {
        if (resp.errno == "0") {
            // 获取城区信息成功
            var areas = resp.data;

            // 遍历城区信息添加到城区下拉列表框
            // for (var i=0; i < areas.length; i++) {
            //     // 获取当前城区
            //     var area = areas[i];
            //
            //     var html = '<option value="' + area.aid +'">' + area.aname + '</option>';
            //     $("#area-id").append(html);
            // }
            var html = template("areas-tmpl", {"areas": areas});
            $("#area-id").html(html);
        }
        else {
            // 获取城区信息失败
            alert(resp.errmsg);
        }
    });

    // TODO: 处理房屋基本信息提交的表单数据
    $("#form-house-info").submit(function (e) {
        e.preventDefault();

        // 获取参数
        var house_params = {};


        $(this).serializeArray().map(function (x) {
            house_params[x.name] = x.value;
        });

        // 获取选中的房屋设施id
        var facility = [];
        $(":checked[name=facility]").each(function (index, item) {
            facility[index] = item.value;
        });

        house_params["facility"] = facility;
        // 请求发布房屋的信息

        $.ajax({
            "url": "/api/v1.0/houses",  // 请求url地址
            "type": "post", // 请求方式，默认是get
            "data": JSON.stringify(house_params), // 请求时传递数据
            "contentType": "application/json",
            "headers": {
                "X-CSRFToken": getCookie("csrf_token")
            },
            "success": function (resp) {
                // 回调函数
                if (resp.errno == "0") {
                    // 发布房屋信息成功
                    // 隐藏发布房屋基本信息表单
                    $("#form-house-info").hide();
                    // 显示上传房屋图片的表单
                    $("#form-house-image").show();
                    // 设置上传房屋图片的表单中房屋id
                    $("#house-id").val(resp.data.house_id);
                }
                else {
                    // 发布房屋信息失败
                    alert(resp.errmsg);
                }
            }
        })

    });
    // TODO: 处理图片表单的数据
    $("#form-house-image").submit(function (e) {
        e.preventDefault();

        // 模拟表单提交操作
        $(this).ajaxSubmit({
            "url": "/api/v1.0/house/image",  // 请求url地址
            "type": "post", // 请求方式，默认是get
            "headers": {
                "X-CSRFToken": getCookie("csrf_token")
            },
            "success": function (resp) {
                // 回调函数
                if (resp.errno == "0") {
                    // 上传房屋图片成功
                    console.log("123")
                    var html = '<img src="' + resp.data.img_url +'">';
                    $(".house-image-cons").append(html);
                }
                else if (resp.errno == "4101"){
                    // 未登录
                    location.href = "login.html"
                }
                else {
                    // 上传房屋图片失败
                    alert(resp.errmsg)
                }
            }
        })

    })
});



