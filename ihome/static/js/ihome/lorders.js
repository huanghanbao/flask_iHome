//模态框居中的控制
function centerModals() {
    $('.modal').each(function (i) {   //遍历每一个模态框
        var $clone = $(this).clone().css('display', 'block').appendTo('body');
        var top = Math.round(($clone.height() - $clone.find('.modal-content').height()) / 2);
        top = top > 0 ? top : 0;
        $clone.remove();
        $(this).find('.modal-content').css("margin-top", top - 30);  //修正原先已经有的30个像素
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function () {
    $('.modal').on('show.bs.modal', centerModals);      //当模态框出现的时候
    $(window).on('resize', centerModals);
    // TODO: 查询房东的订单
    $.get("/api/v1.0/orders?role=landlord", function (resp) {
        if (resp.errno == "0") {
            // 成功
            var html = template("orders-list-tmpl", {"orders": resp.data});
            $(".orders-list").html(html);

            // TODO: 查询成功之后需要设置接单和拒单的处理
            $(".order-accept").on("click", function () {
                var orderId = $(this).parents("li").attr("order-id");
                $(".modal-accept").attr("order-id", orderId);
            });

            // 接单操作
            $(".modal-accept").click(function (resp) {
                // 获取订单id
                var order_id = $(this).attr("order-id");

                // 接单请求
                $.ajax({
                    "url": "api/v1.0/order/" + order_id + "/status?action=accept",  // 请求url地址
                    "type": "put", // 请求方式，默认是get
                    "headers": {
                        "X-CSRFToken": getCookie("csrf_token")
                    },
                    "success": function (resp) {
                        // 回调函数
                        if (resp.errno == "0") {
                            // 接单成功
                            // 1. 设置订单状态的html
                            $(".orders-list>li[order-id=" + order_id + "]>div.order-content>div.order-text>ul li:eq(4)>span").html("已接单");
                            // 2. 隐藏接单和拒单操作
                            $("ul.orders-list>li[order-id=" + order_id + "]>div.order-title>div.order-operate").hide();
                            // 3. 隐藏弹出的框
                            $("#accept-modal").modal("hide");
                        }
                        else if (resp == "4101") {
                            // 用户未登录，跳转到登录页面
                            location.href = "login.html";
                        }
                        else {
                            // 出错
                            alert(resp.errmsg);
                        }
                    }
                })
            });

            $(".order-reject").on("click", function () {
                var orderId = $(this).parents("li").attr("order-id");
                $(".modal-reject").attr("order-id", orderId);
            });

            // 拒单操作
            $(".modal-reject").click(function () {
                // 获取订单id
                var order_id = $(this).attr("order-id");

                // 获取拒单原因
                var reason = $("#reject-reason").val();

                var params = {
                    "reason": reason
                };

                // 请求拒单
                $.ajax({
                    "url": "api/v1.0/order/" + order_id + "/status?action=reject",  // 请求url地址
                    "type": "put", // 请求方式，默认是get
                    "contentType": "application/json", // 请求数据的格式
                    "data": JSON.stringify(params), // 请求时传递数据
                    "headers": {
                        "X-CSRFToken": getCookie("csrf_token")
                    },
                    "success": function (resp) {
                        // 回调函数
                        if (resp.errno == "0") {
                            // 拒单成功
                                // 1. 设置订单状态的html
                                $(".orders-list>li[order-id="+ order_id +"]>div.order-content>div.order-text>ul li:eq(4)>span").html("已拒单");
                                // 2. 隐藏接单和拒单操作
                                $("ul.orders-list>li[order-id="+ order_id +"]>div.order-title>div.order-operate").hide();
                                // 3. 隐藏弹出的框
                                $("#reject-modal").modal("hide");
                        }
                        else if (resp.errno == "4101") {
                            // 用户未登录，跳转到登录页面
                            location.href = "login.html";
                        }
                        else {
                            // 出错
                            alert(resp.errmsg);
                        }
                    }
                })
            })
        }
        else if (resp.errno = "4101") {
            // 用户未登录，跳转到登录页面
            location.href = "login.html";
        }
        else {
            // 出错
            alert(resp.errmsg);
        }
    });
});
