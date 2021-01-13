# 学工平台每日上报

[![PyPI version](https://img.shields.io/pypi/v/yqxx)](https://pypi.org/project/yqxx/)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/billchenchina/yqxx)](https://github.com/billchenchina/yqxx/releases)
[![GitHub stars](https://img.shields.io/github/stars/billchenchina/yqxx)](https://github.com/billchenchina/yqxx/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/billchenchina/yqxx)](https://github.com/billchenchina/yqxx/network)
[![GitHub issues](https://img.shields.io/github/issues/billchenchina/yqxx)](https://github.com/billchenchina/yqxx/issues/)

本项目为命令行填报哈尔滨工业大学[学工平台](https://xg.hit.edu.cn/)[每日上报](https://xg.hit.edu.cn/zhxy-xgzs/xg_yqglxs/xsmrsb)的工具。实现了[统一身份认证登录](http://ids.hit.edu.cn/authserver/login)、获取所有上报信息、按照配置文件自动上报功能。

## 如何使用

0. `pip install yqxx`
1. 按照下面模板填写账号密码等信息
2. 运行 `yqxx -c <配置文件名>`

<!-- 如需定时执行，请自行配置任务计划（Windows）或 Cron 任务（Linux） -->

## 配置文件模板

配置文件为 YAML 格式，对配置文件进行编辑后保存到本地：

```yaml
# 统一身份认证账号
username: '1234567890'
# 统一身份认证密码
password: 'PASSWORD'
# 体温
brzgtw: '36.5'
# 国（境）内详细地址
gnxxdz: '黑龙江省哈尔滨市南岗区工建街88号哈工大招待所'
# 当前状态
# 01 在校（校内宿舍住）
# 03 居家
# 04 探亲
# 05 访友
# 06 旅行
# 07 会议
# 99 其他
dqztm: '03'
# 当前所在区
# 为当前所在区的行政区划代码（即身份证号前六位）
dqszdqu: '230103'
```

## 开源许可证

[AGPL-3.0](./LICENSE)

简单来说，建议您做到以下几点：

- 任何基于或与本项目有间接接触的项目均使用AGPL-3.0协议
- 当你使用本项目或对其修改时，如果你所服务的对象向您索要源代码，请不要拒绝
- 请不要将本项目用于商业用途

## 免责声明

本项目仅为方便通过命令行进行每日上报的工具。按照 [LICENSE](./LICENSE)，开发者不对本工具的使用负责。
