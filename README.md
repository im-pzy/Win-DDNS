# 概览
本项目是对Windows系统开发的腾讯云DDNS（动态域名解析服务）程序，原理是通过任务计划间隔检测IP的变化，通过API及时更新到云端，日志记录并通过webhook推送到企业微信机器人方便手机查看，项目分为三个部分：
- `config.json`：配置文件
- `DDNS.ps1`：DDNS基本程序，负责检测IP变化、启动云端通信程序、日志记录
- `DDNS.xml`：任务计划文件
- `update_DDNS.py`：云端通信程序，负责更新IP、推送消息



# config.json参数说明
*InterfaceIndex*
在PowerShell中输入命令`Get-NetAdapter`，找到对应网卡的`ifIndex`

*IPType*
有SLAAC（本地链接IPv6）、DHCP（本地链接IPv6）、TEMP（临时IPv6）、IPv4四种类型，前三种都是针对IPv6的，IPv6推荐使用TEMP，因为SLAAC有泄露物理地址的风险。

*临时IP开启方式*
```
开启临时IP：netsh interface ipv6 set privacy state=enable
修改临时IP最大首选寿命（不然会每天一变）：netsh interface ipv6 set privacy maxpreferredlifetime=7d
关闭临时IP：netsh interface ipv6 set privacy state=disable
```

*Domain、SubDomain*
- `Domain`：域名，例如`xxx.com`
- `SubDomain`：子域名（主机名），例如`www`、`host`，如果项目使用根域名，则填`@`

*SecretId、SecretKey*
腾讯云密钥，在控制台生成和查看

*WebhookKey*
企业微信机器人的key，在群聊中点击机器人信息即可查看



# 导入任务计划
将文件导入任务计划，导入时注意修改任务的用户名、脚本路径(DDNS.ps1)、工作路径

# 安装python模块
`pip install -r requirements.txt`