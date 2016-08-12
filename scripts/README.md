# 生成路由表和动态DNS的脚本

## 背景

相关背景请参看 [https://haoel.github.io/](https://haoel.github.io/)

## 生成

简单运行如下命令：

```
./build.sh
```

注释：

- 在 `../downloads/` 目录下生成 `route.sh` 、 `wan-start` 和 `dnsmasq.conf.add`三个文件 。

- 该脚本会从 [https://github.com/17mon/china_ip_list](https://github.com/17mon/china_ip_list) 下载中国区的网段，从 [https://github.com/felixonmars/dnsmasq-china-list](https://github.com/felixonmars/dnsmasq-china-list) 下载DNS表

- 该脚本会对dnsmasq.conf.add中加入 `itunes.apple.com` ，并去除 Linkedin 的 CDN `static.licdn.com`

- 目录中的 `route_base.sh` 是生成的 `route.sh` 的模板

## 复制生成的文件到路由器上

- 把 `route.sh` 和 `wan-start` 拷贝到路由的 `/jffs/scripts` 下

- 把 `dnsmasq.conf.add` 拷贝到路由器的 `/jffs/configs` 下

```
cd ../downloads/
scp route.sh wan-start admin@192.168.1.1:/jffs/scripts
scp dnsmasq.conf.add admin@192.168.1.1:/jffs/configs
```

## 生效路由表和动态DNS

```
> ssh admin@192.168.1.1 
> admin@192.168.1.1's password: ******
>
> chmod a+rx /jffs/scripts/*
> /jffs/scripts/route.sh add
> service restart_dnsmasq
```
