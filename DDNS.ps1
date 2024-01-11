$config = Get-Content config.json | ConvertFrom-Json
$lastIPFile = 'last_ip.txt'
$logFile = 'log.txt'

# 获取IP地址
switch ($config.IPType) {
    "SLAAC" {$currentIP = (Get-NetIPAddress -InterfaceIndex $config.InterfaceIndex -AddressFamily IPv6 -AddressState Preferred -PrefixOrigin RouterAdvertisement -SuffixOrigin Link).IPAddress}
	"DHCP" {$currentIP = (Get-NetIPAddress -InterfaceIndex $config.InterfaceIndex -AddressFamily IPv6 -AddressState Preferred -PrefixOrigin Dhcp -SuffixOrigin Dhcp).IPAddress}
	"TEMP" {$currentIP = (Get-NetIPAddress -InterfaceIndex $config.InterfaceIndex -AddressFamily IPv6 -AddressState Preferred -PrefixOrigin RouterAdvertisement -SuffixOrigin Random).IPAddress}
	"IPv4" {$currentIP = (Get-NetIPAddress -InterfaceIndex $config.InterfaceIndex -AddressFamily IPv4 -AddressState Preferred).IPAddress}
}

# last_ip.txt不存在则创建
if (-not (Test-Path -Path $lastIPFile -PathType Leaf)) {
    Set-Content -Path $lastIPFile -Value $currentIP
}

# 读取上一次检测记录的IP
$lastIP = Get-Content $lastIPFile

# 如果IP发生变化
if ($currentIP -ne $lastIP) {
    # 修改DNS记录
    $res = python update_DDNS.py -i $currentIP
    # 修改last_ip.txt
    Set-Content -Path $lastIPFile -Value $currentIP
    # 记录IP变化日志
    Add-Content -Path $logFile -Value "$(Get-Date): $res"
}