import json
import argparse
import requests
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.dnspod.v20210323 import dnspod_client, models

# 读取配置
config_file = open("config.json")
config = json.load(config_file)
config_file.close()

# 接收参数
parser = argparse.ArgumentParser(description='receive IPAddress')
parser.add_argument('--IP','-i',type=str,required=True,help="IPAddress")
args = parser.parse_args()

webhookurl = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key="+config["WebhookKey"]

try:
    cred = credential.Credential(config["SecretId"], config["SecretKey"])
    httpProfile = HttpProfile()
    httpProfile.endpoint = "dnspod.tencentcloudapi.com"
    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    client = dnspod_client.DnspodClient(cred, "", clientProfile)

    # 请求RecordId
    req = models.DescribeRecordListRequest()
    params = {
        "Domain": config["Domain"],
        "Subdomain": config["SubDomain"],
        "RecordType": "AAAA"
    }
    req.from_json_string(json.dumps(params))
    resp = client.DescribeRecordList(req)
    recordId = resp.RecordList[0].RecordId

    # 更新DDNS
    req = models.ModifyDynamicDNSRequest()
    params = {
        "Domain": config["Domain"],
        "SubDomain": config["SubDomain"],
        "RecordId": recordId,
        "RecordLine": "默认",
        "Value": args.IP
    }
    req.from_json_string(json.dumps(params))
    resp = client.ModifyDynamicDNS(req)

    # 推送到企业微信机器人
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "msgtype": "text",
        "text": {
            "content": "您的IP已更新为"+args.IP
        } 
    }
    res = requests.post(webhookurl, headers=headers, json=data)
    print("IP Changed to "+args.IP)


except TencentCloudSDKException as err:
    # 推送到企业微信机器人
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "msgtype": "text",
        "text": {
            "content": str(err)
        } 
    }
    res = requests.post(webhookurl, headers=headers, json=data)
    print(err)
