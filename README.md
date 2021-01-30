## 疫情无小事,防控靠大家。真的有什么状况即时上报

## 食用方法

- 1.首先保证你有一个GitHub账号

- 2.fork一份到自己仓库

- 3.打开settings，找到secrets，新建secret如下
| secret_iD   | value                   |
| ----------- | ----------------------- |
| PHONE       | 登录手机号              |
| PASSWORD    | 登录密码                |
| ADDRESS     | 打卡定位地址            |
| LAT         | 纬度                    |
| LNG         | 经度                    |
| DEVICETOKEN | 你抓包得到的devicetoken |
| SCKEY       | sever酱                 |
- 4.DEVICETOKEN获取方法。
[操作视频](https://mp.weixin.qq.com/s/9ww2373nxj3JyV4o1VAvAw)

- 5.sever酱使用参见[官网](http://sc.ftqq.com/3.version)。

- 6.开启 Actions 并触发每日自动执行
Github Actions 默认处于关闭状态，大家请手动开启 Actions ，执行一次工作流，验证是否可以正常工作。
[图片](https://s3.ax1x.com/2021/01/27/sxz1IJ.png)

- 7.如果需要修改每日任务执行的时间，请修改 `.github/workflows/autoClockIn.yml`，在第 8 行左右位置找到下如下配置。

```yml
  schedule:
    - cron: '10 21 * * *'
    # cron表达式，Actions时区是国际时间，国际时间21点的时候，国内时间是5点。
    # 示例： 每天早上5点10分执行 '10 21 * * *'
```

- 8.经纬度可以进入[高德地图API](https://developer.amap.com/api/webservice/guide/api/georegeo#geo)下翻至服务示例，输入你的定位地点后于返回的数据中获取
[点我看图](https://s3.ax1x.com/2021/01/28/y9Ml5Q.png)

### Q群：[点击链接加入群聊](https://jq.qq.com/?_wv=1027&k=oCdISxo1)
