# 用 ASUS Merlin 路由器 VPN 科学上网

作者：左耳朵 [http://coolshell.cn](http://coolshell.cn)
更新时间：2016-08-10

这篇文章及其脚本可以写的更好，欢迎到 [https://github.com/haoel/haoel.github.io](https://github.com/haoel/haoel.github.io) 更新

## 准备

### 首先，你应该对英文读写没什么问题

为什么这么说？**逻辑是这样的，如果你上了Google还是在用中文关键词，那么你科学上网有什么意义呢？** 换言之，科学上网的目的是为了进入广阔的世界范围与全世界的人交流，所以，英文是必备的，如果你英文有问题，VPN过去也的用处也不大。

所以，我把这个前提条件放在第一的位置，就是说—— **真正的墙不是GFW，而是人的大脑**


### 然后，你需要一个VPN

这里我用的是PPTP，可以上AWS日本申请个免费试用一年的EC2 VPS，或是Linode买个一月USD10刀的VPS，然后自建一个PPTP的VPN。

我在北京，感觉日本的VPS是比较快，其本上ping值可以在100ms以内，linode的似乎可以在50ms左右。Anyway，**现在你买一台VPS也不贵了，也就是一个月10美金左右（60-70元），千万别告诉我，一个月你花60-70元钱对你是件很奢侈的事**。

关于PPTP服务器的设置，请参看 《[How To Setup Your Own VPN With PPTP](https://www.digitalocean.com/community/tutorials/how-to-setup-your-own-vpn-with-pptp)》

### 最后，你需要一台ASUS的路由器 

用这台路由器的目的是为了用路由器科学上网，这样全家或全公司就科学上网了。

朋友安利我的是 **华硕（ASUS） RT-AC68U 1900M AC 双频智能无线路由路**，可能这个路由器对你来说有点贵，你也可以看看别的，比如：RT-AC66U，大约600元。

当然，不用这样的路由器也没有什么问题，在所有的客户端设备上设置VPN也没有问题。

## 路由器设置

### 给路由器刷 merlin 固件

首先Asuswrt是华硕公司为他的路由器所开发的固件。Asuswrt-merlin是一个对Asuswrt固件二次开发进行各种改进和修正的项目。源代码在这里：[https://github.com/RMerl/asuswrt-merlin](https://github.com/RMerl/asuswrt-merlin)

Merlin固件拥有更多的功能，由于第三方不断维护代码，各种新功能也在不断增加。Merlin固件的升级并不需要反复的操作过程，方法与官方固件的升级相同，有很好的硬件软件兼容性。继承了Asuswrt官方固件优秀的交互界面。

另外，不必担心把路由器刷废了，华硕的路由器可以让你一键重置回来

**1）下载固件**。先到 [https://asuswrt.lostrealm.ca/download](https://asuswrt.lostrealm.ca/download) 下载相应的固件，并解压。（我下载的是 `RT-AC68U_380.61_0.zip` ）

**2）升级固件**。登录到你的路由器后台 `http://192.168.1.1/` ，在 `系统管理` -> `固件升级` 中上传固件文件（我上传的是：`RT-AC68U_380.61_0.trx`）

**3）打开 JFFS 分区**。`系统管理` -> `系统设置` -> `Persistent JFFS2 partition`

- `Format JFFS partition at next boot` - `否`
- `Enable JFFS custom scripts and configs` - `是`


**4）打开 ssh 登录**。 `系统管理` -> `系统设置` -> `SSH Daemon` 

- `Allow SSH password login` - `是`


### 连接 VPN

**1）到 `VPN` -> `PPTP/L2TP Client` 中 添加设置文件。**

注：最好使用PPTP，设置起来比较简单。L2TP不支持PEK的共享密码。

**2）保存配置后，点 `Active`， 如果一切正确，可以看到连接成功。**


### 设置路由

此时，你的路由器就VPN了，但是，包括访问中国的网站也被代理了。所以，还要设置一下路由表。


```
ssh admin@192.168.1.1
```

输入你设置的路由器后台的登录口令，你就可以进入路由器的操作系统了。

#### 下载路由表

**为什么要设置路由表？**

路由器VPN后，你所有的网络访问都得多国外绕一圈了。所以，需要把国内的IP给过滤出来，所以，需要设置静态路由表。

```
cd /jffs/scripts
wget https://haoel.github.io/downloads/route.sh
echo -e "#!/bin/sh\n\n/jffs/scripts/route.sh delete\n/jffs/scripts/route.sh add" > /jffs/scripts/wan-start
chmod a+rx /jffs/scripts/*
```
**wan-start 是什么？**

注：`wan-start` 是一个事件脚本，在wan口连上后会运行，这里的运行指令是，先删除路由，再加入（因为WAN口的IP可能会换了）

**route.sh 怎么来的？**

- 这个脚本的路由表是由来高春辉的这个项目。 [https://github.com/17mon/china_ip_list](https://github.com/17mon/china_ip_list) （之前的[https://github.com/fivesheep/chnroutes](https://github.com/fivesheep/chnroutes) 已经没有人维护）
- 这个脚本包含5000多条路由规则，几乎包括了中国的网段。
- 我使用这个配置生成了 `route.sh` （生成脚本 [https://github.com/haoel/haoel.github.io/tree/master/scripts](https://github.com/haoel/haoel.github.io/tree/master/scripts) ）
- 你可以使用 `route.sh add` 来生效路由表，用 `./route.sh delete` 来删除路由表。


#### 下载动态DNS配置

**为什么要设置动态DNS？**

因为很多网站都会使用CDN，使用CDN的通常都会用DNS的CNAME做解析，所以，你的路由器VPN后，你的DNS服务器也会变了，我们这里默认使用的是Google的8.8.8.8，当然，这台服务器在国外，所以，用这台服务器解析域名的时候，就会解析到国外。所以，我们还需要一个动态的DNS配置，对于国内的站点，使用国内的DNS，对于国外的站点，使用8.8.8.8

```
cd /jffs/configs
wget https://haoel.github.io/downloads/dnsmasq.conf.add
```

**dnsmasq.conf.add怎么来的？**

- 这个配置来自 [https://github.com/felixonmars/dnsmasq-china-list](https://github.com/felixonmars/dnsmasq-china-list)
- 因为似乎他没有加上 itunes.apple.com ，所以，我就简单的把 `server=itunes.apple.com/114.114.114.114` 加到了 `accelerated-domains.china.conf` ，然后直接改名为 dnsmasq.conf.add
- 另外，`linkedin.com` 使用到的 `static.licdn.com` 也在这个文件中，建议去掉，不然linkedin.com打开会因为找不到相应的资源文件而异常。
- 生成脚本 [https://github.com/haoel/haoel.github.io/tree/master/scripts](https://github.com/haoel/haoel.github.io/tree/master/scripts) 

_注：文件里用到的是 `114.114.114.114` 作为国内的DNS解析服务。经网友指出这个不靠谱 [http://bobao.360.cn/news/detail/1793.html](http://bobao.360.cn/news/detail/1793.html)_

你可以在路由器上通过 `nvram get wan0_dns` 查看你自己的DNS，然后替换掉，如：

```
sed -i "s/114.114.114.114/$(nvram get wan0_dns|awk '{print $1}')/" dnsmasq.conf.add
```


#### 运行命令生效

```
/jffs/scripts/route.sh add 
service restart_dnsmasq
```

接下来，你需要让你的设备重新连接一下WiFi路由器。

#### 检查

你可以使用一些命令在检查，相应的域名是否被CNAME到了正确的地方。

如：

```
nslookup itunes.apple.com
```

```
ping www.google.com
```

```
traceroute weibo.com
```

然后查一查相关的IP是的位置在哪个国家。

## 已知问题

### QUIC 的问题

使用上述配置，在使用Chrome访问Googlet系统的网站时，比如：www.google.com、www.youtube.com 会出现打不开页面的问题。我做了一些调查，发现，这个问题是和Google的 [QUIC](https://en.wikipedia.org/wiki/QUIC) 协议相关，因为Safari和FireFox是没有这个问题的，因为Safari和Firefox用的是HTTPS而不是QUIC。

Workaround的方式是 Disable Chrome的试验型的QUIC协议，在Chrome里访问 `chrome://flags/#enable-quic` 可以关闭QUIC。

目前，我在ASUS Merlin的官方论坛发了个贴：[http://www.snbforums.com/threads/quic-issue.34105/](http://www.snbforums.com/threads/quic-issue.34105/)

（全文完）







