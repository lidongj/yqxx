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

# 经度
gpsjd: 126.630644
# 纬度
gpswd: 45.746883

# 居住地址（Residence Address）（请详细填写至门牌号，如：X省X市X区X街X小区/楼宇X单元X门牌号）(Road and doorplate，e.g.：Room XX No. XX Community XX)
# 走读需要填写
jzdz: ''

# 所在地点（Currrent location）
# 0 国（境）外（Overseas）
# 1 国内（Domestic）
kzl1: 1

# 所在国家或地区（Current Country or region Residing in）
# 国（境）外（Overseas）需要填写
kzl2: ''

# 所在国家城市（Current City Residing in）
# 国（境）外（Overseas）需要填写
kzl3: ''

# 所在国家具体地址（Address Residing in）
# 国（境）外（Overseas）需要填写
kzl4: ''

# 近1个月是否计划回国（Do you plan to return to China within one month）
# 国（境）外（Overseas）需要填写
# 0 否
# 1 是
kzl5: ''

# 定位信息建议通过 https://lbs.amap.com/demo/javascript-api/example/geocoder/regeocoding F12 获取
# 定位省
kzl6: '黑龙江省'

# 定位市
# 直辖市留空
kzl7: '哈尔滨市'

# 定位区
kzl8: '南岗区'

# 定位详细地址
# 街道名+门牌号
kzl9: '教化街30号'

# 定位信息
# 地图定位地点
kzl10: '黑龙江省哈尔滨市南岗区花园街道教化街哈尔滨工业大学'

# 与上次定位在不同城市的原因
# 0 探亲（Visiting relatives）
# 1 旅游（Traveling）
# 2 回家（Homecoming）
# 3 因公出差/实习实训（Business /practical reasons）
# 4 其他（Others）
kzl11: ''

# 与上次定位在不同城市的原因
kzl12: ''

# 您当前所在地点是（Your current location is）(单元/社区/街道等) (unit/community/street, etc.)
# 0 低风险地区（Low risk area）
# 1 中风险地区（Medium risk area）
# 2 高风险地区（High risk areas）
kzl13: 0

# 您所处中/高风险地区所在街道，社区名称（The street and community name of your medium/high risk area is）
# 例：哈尔滨市呼兰区兰河街道沿河社区
kzl14: ''

# 当日是否途径中高风险地区（Any contact with medium or high risk area?）
# 0 否
# 1 是
kzl15: 0

# 中/高风险地区所在街道，社区名称（The street and community name of medium/high risk area is）
# 例：哈尔滨市呼兰区兰河街道沿河社区
kzl16: ''

# 今日体温范围（Today's temperature）
# 0 37.2℃及以上（Greater then or equal to 37.2°C；）
# 1 37.2°C以下（ below 37.2°C）
kzl17: 1

# 今日是否出现不适（多选）？（Do you have any of the following symptoms（Multiple choice）?）
# 0 无不适（Asymptomatic）
# 1 乏力（Fatigue）
# 2 干咳（Dry cough）
# 3 呼吸困难（Difficulty in breathing）
# 4 其他（Other symptoms）
kzl18: '0;'

# 是否到相关医院或门诊检查（Did you go to a hospital or clinic for a check-up?)
# 0 否
# 1 是
kzl19: ''

# 检查结果（Examination results)
# 0 疑似感染（Suspected）
# 1 确诊感染（Infected）
# 2 其他（Others）
kzl20: ''

# 自行采取的救护措施？（Has any medications been taken by oneself?）
# 0 已口服药物，无其他异常(Already took oarl medication, no other symptoms)
# 1 未服药物，无其他异常（Didn't take any medications, no other symptoms)
# 2 其他情况（Other situations）
kzl21: ''

# 其他情况（Other situations）
kzl22: ''

# 当前的健康状况（Current health status）
# 0 正常（Normal）
# 1 新冠肺炎无症状感染者（Novel coronavirus pneumonia asymptomatic infection）
# 2 新冠肺炎确诊病例（Confirmed cases of novel coronavirus pneumonia）
kzl23: 0

# 是否处于隔离期？（Are you currently in an isolation period?）
# 0 否
# 1 是
kzl24: 0

# 隔离场所（Isolation place）
# 0 定点医院（Designated hospital）
# 1 集中隔离点（Centralized isolation location）
# 2 居家隔离（Isolate at home）
kzl25: ''

# 隔离详细地址（The detailed address of isolation）
# （请填写隔离医院/集中隔离点/居家隔离详细地址，精确到门牌号）(please fill in the detailed address of the isolated hospital/centralized isolation location/isolated at home, accurate to the door number)
kzl26: ''

# 隔离开始时间（Start date of isolation）
# 示例：2021-8-15
kzl27: ''

# 本人或共同居住的家人是否与确诊病例、无症状感染者、疑似病例行程轨迹有交集？（Do you or your family members living together cross paths with confirmed /asymptomatic/ suspected cases?）
# 0 否（No）
# 1 是（Yes）
kzl28: 0

# 是否与确诊病例、无症状感染者乘坐同次航班和列车（Has a confirmed or asymptomatic case  been detected in same transportation with you）
# 0 否（No）
# 1 是（Yes）
kzl29: ''

# 请详细说明（Please specify）
kzl30: ''

# 本人48小时内是否已进行核酸检测（Has COVID-19 nucleic acid test been conducted during 48 hours）
# 0 否（No）
# 1 是（Yes）
kzl31: ''

# 目前本人新冠疫苗接种情况（Vaccination status）
# 0 未接种(Unvaccinated)
# 1 已接种部分剂次(Single dose has been inoculated)
# 2 已接种全部剂次(Both doses inoculated)
kzl32: 0

# 其他信息（Other information）
kzl33: '无'
# 省(名称)
kzl38: '黑龙江省'
# 市(名称)
# 直辖市留空
kzl39: '哈尔滨市'
# 区(名称)
kzl40: '南岗区'
```

## 开源许可证

[AGPL-3.0](./LICENSE)

简单来说，建议您做到以下几点：

- 任何基于或与本项目有间接接触的项目均使用AGPL-3.0协议
- 当你使用本项目或对其修改时，如果你所服务的对象向您索要源代码，请不要拒绝
- 请不要将本项目用于商业用途

## 免责声明

本项目仅为方便通过命令行进行每日上报的工具。按照 [LICENSE](./LICENSE)，开发者不对本工具的使用负责。
