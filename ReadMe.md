支付宝网页支付demo
====
[toc]

> 项目基于django，开发通过支付宝网页支付接口，完成待支付订单的支付业务。

## 简单业务流程
1. 用户通过网页发起商品结算支付请求
2. 后端收到请求生成待支付订单, 重定向用户到支付宝网页收银台
3. 用户在支付宝网页收银台完成支付
4. 支付宝重定向用户到我方的支付完成页面
5. 于此同时支付宝异步调用我方的订单完成接口
6. 我方订单完成接口收到支付宝异步回调后，更改订单状态。
7. 由于返回支付完成页面和更改订单状态两个行为是异步的，所以理论上应该是订单状态改变在先，但是订单完成页面在后。由于异步，所以可能存在数据库中
订单状态还未即使修改，用户已经先达到支付完成页面，所以对于支付完成页面可以进行订单查询或轮询订单状态，然后再展示用户订单完成信息。

## demo视图
1. 结算支付请求发起视图
2. 支付宝异步回调修改订单状态视图
3. 支付宝支付成功通过回调视图

## 数据库model
1. 账号表
2. 订单表

## 支付宝网页支付，支付宝端配置
1. 由于是demo测试，所以利用支付宝沙箱环境，登陆沙箱环境，支付宝自动生成测试appid等信息。
2. 生成我方应用的rsa算法的公私钥，将应用公钥存入沙箱环境。
3. 下载保存支付宝沙箱环境的支付宝公钥。
4. 记下我们的appid。
5. 下载支付宝沙箱app，查看沙箱用户账号信息，并用于登陆沙箱app，然后充值沙箱余额后续用于支付。

## 支付宝网页支付调用参数逻辑
1. 我方的订单信息：商品信息/我方订单号/支付金额
2. 我方账号信息：appid/(公钥私钥，隐含签名代表身份支付宝卖家账号)
3. 支付接口相关信息：  "method": method,
                    "charset": "utf-8",
                    "sign_type": "RSA2",
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "version": "1.0",
4. 排序然后利用应用私钥签名所有信息。
5. 将签名加入到参数列表，将参数列表发送给支付宝沙箱接口。

具体逻辑看代码。

### 参数列表生成和签名及验签
都是利用utils.sdk.alipay模块中的功能。模块的依赖说明在模块注释中有说明。主要依赖pip install pycryptodome 模块


## 支付宝回调参数展示
### 异步回调POST请求内容
```
 {
 'gmt_create': '2019-04-12 09:24:12', 
 'charset': 'utf-8', 
 'gmt_payment': '2019-04-12 09:24:29', 
 'notify_time': '2019-04-12 09:24:31', 
 'subject': 'Python全栈课程24个月;Linux运维',
 'sign': 'L4mjL8jFVWRdj5Sux0lKCm/Sy5zzNMlYcCzOX+1K+HcdAwmixz1NpDUSRYt7znQQwFl/T3YzDp7xZNU1Wlzo2z60g0kzaUDV/vOlC38isSmIys9A2jQvwjCmQT7nSwKcpIlr2KW6SR0UA4eh9BwRZymzskkgvVexuabol5KFtAYfodYJtnKZbeWZW/FIrtBc+Nc0dbk+WWfjtIwRicLAKPEI97LzsK2QhGVxUpe/jn6gFj1mn+TWPGUpRz4EcyqGF8HBFvovMTjeXIfOKbdu0+Ju4hgfFZs2+KIIleTt2M3MRm04IhUGrGmS7thClyD64tmex8Xh3F7VdzR8VN9M9A==', 
 'buyer_id': '2088102177254584', 
 'invoice_amount': '1000.00', 
 'version': '1.0', 
 'notify_id': '2019041200222092429054581000088563',
 'fund_bill_list': '[{
					  "amount":"1000.00",
					  "fundChannel":"ALIPAYACCOUNT"
					  }]', 
 'notify_type': 'trade_status_sync', 
 'out_trade_no': '45883ab2-94a7-497f-ab1d-34b9190e4fea', 
 'total_amount': '1000.00', 
 'trade_status': 'TRADE_SUCCESS', 
 'trade_no': '2019041222001454581000011472', 
 'auth_app_id': '2016092200572114', 
 'receipt_amount': '1000.00', 
 'point_amount': '0.00', 
 'app_id': '2016092200572114', 
 'buyer_pay_amount': '1000.00', 
 'sign_type': 'RSA2',
 'seller_id': '2088102176803381'
 }
```

## 项目运行部署
1. 必须在公网，因为支付宝时公网回调。建议购买一个ECS开发测试