# VPN 科学上网

作者：左耳朵 [http://coolshell.cn](http://coolshell.cn)
更新时间：2018-11-29

这篇文章及其脚本可以写的更好，欢迎到 [https://github.com/haoel/haoel.github.io](https://github.com/haoel/haoel.github.io) 更新

## 1. 英文能力

**首先，你应该对英文读写没什么问题**

为什么这么说？**逻辑是这样的，如果你上了Google还是在用中文关键词，那么你科学上网有什么意义呢？** 换言之，科学上网的目的是为了进入广阔的世界范围与全世界的人交流，所以，英文是必备的，如果你英文有问题，VPN过去也的用处也不大。

所以，我把这个前提条件放在第一的位置，就是说—— **真正的墙不是GFW，而是人的大脑**


## 2. 购买VPS

然后，你需要一个VPS

**现在你买一台VPS也不贵了，也就是一个月10美金左右（70元），我个人一个月你花70元钱不算奢侈的事，而且会让你的生活质量得得改善**。

### 2.1 常规VPS

对于VPS，下面是一些常规选项。

- 上[AWS](https://aws.amazon.com/cn/)日本或韩国申请个免费试用一年的EC2 VPS （需要国际信用卡）
- 上[Linode](https://www.linode.com)买个一月USD10刀的VPS
- 上[Vultr](https://www.vultr.com)上买一个日本的VPS，一个月5刀 （可以支付宝）
- 上[Conoha](https://www.conoha.jp/zh/)上买一个日本的VPS，一个月900日元 （可以支付宝）

注意，日本区的网络质量并不是很好，有时候会有很大的丢包率（不同的网络不一样），有时候会很慢。上述的这几个VPS服务商中，AWS韩国和日本会好点，然后是Linode，最后是Conoha和Vultr（如果你有更好的，请推荐）

### 2.2 CN2 线路

如果你需要更好更高速的网络服务（比如你要看Youtube的1080P），那么，你需要下面的这些服务器资源了（价格也会高一些）

`CN2` 和 `GIA` 是两个关键词。CN2 GIA全称Chinatelecom Next Carrier Network- Global Internet Access 电信国际精品网络，特征是路由线路上骨干节点均为59.43开头的IP。如果想要寻找接入CN2线路的国外VPS提供商，建议使用 `Next Carrier Network` 或者 `CN2` 这个关键词搜索即可。

多说一句， CN2本身又分为两种类型：

- CN2 GT: CN2里属于Global Transit的产品(又名GIS-Global Internet Service)，在CN2里等级低，省级/出国节点为202.97开头，国际骨干节点有2～4个59.43开头的CN2节点。在出国线路上拥堵程度一般，相对于163骨干网的稍强，相比CN2 GIA，性价比也较高。

- CN2 GIA: CN2里属于Global Internet Access的产品，等级最高，省级/出国/国际骨干节点都以59.43开头，全程没有202.97开头的节点。在出国线路上表现最好，很少拥堵，理论上速度最快最稳定，当然，价格也相对CN2 GT偏高。
 
关于 `CN2` 线路的主机提供商，下面罗列几个（更多的可以参考这篇文章《[CN2 GIA VPS主机收集整理汇总-电信,联通,移动三网CN2 GIA线路VPS主机](https://wzfou.com/cn2-gia-vps/)》）

- [搬瓦工](https://bandwagonhost.com/aff.php?aff=39384) 
- [Gigsgigscloud](https://clientarea.gigsgigscloud.com/index.php?/cart/cloudlet-v-hk/&step=0) CN2 GIA 在香港的结点是很不错的，当然，价格也很不错（建议几个人一起平摊费用）
- [Kvmla](https://www.kvmla.com/) 香港地区的CN2 GIA提供商 每月80元
- [Hostdare](https://manage.hostdare.com/index.php) 

重点说一下，CN2 GIA + 香港机房，你会得到巨快无比的上网速度，在Youtube.com上看1080p的视频毫无压力。虽然阿里云和腾讯的也有，但是被查到的风险基本上是100%，不建议使用，被抓了别怪我没警告过你。



## 3. VPN 和 Shadowsocks 服务

### 3.1 设置Docker服务

首先，你要安装一个Docker CE 服务，这里你要去看一下docker官方的安装文档：

- [CentOS 上的 Docker CE 安装](https://docs.docker.com/install/linux/docker-ce/centos/)
- [Ubuntu 上的 Docker CE 安装](https://docs.docker.com/install/linux/docker-ce/ubuntu/)

然后开始设置你的VPN/SS服务

### 3.2 设置Shadowsocks服务

下面命令行中被 `{` 和 `}` 引用的地方，需要替换一下：

```
sudo docker run -d -p 1984:1984  -s 0.0.0.0 -p 1984 \
                -k {密码} -m aes-256-cfb \
                oddrationale/docker-shadowsocks
```



### 3.3 设置L2TP/IPSec服务

下面命令行中被 `{` 和 `}` 引用的地方，需要替换一下：

```
sudo docker run -d -p 500:500/udp -p 4500:4500/udp -p 1701:1701/tcp \
                -e PSK={共享密码} -e USERNAME={用户名}-e PASSWORD={密码}\
                siomiz/softethervpn
```

### 3.4 设置PPTP服务

PPTP不安全，请慎重使用

```
sudo docker run -d --privileged --net=host 
                -v {/path_to_file/chap-secrets}:/etc/ppp/chap-secrets \
                mobtitude/vpn-pptp
```
PPTP 使用 `/etc/ppp/chap-secrets` 文件设置用户名和密码，所以你需要给docker容器提供这个文件，下面是这个文件的示例：

```
# Secrets for authentication using PAP
# client    server      secret           acceptable local IP addresses
  fuckgfw   *           whosyourdaddy    *
```



（全文完）







