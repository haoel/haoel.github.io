    "outbounds": [
      {
        "tag":"IP4_out", //IPv4优先
        "protocol": "freedom",
        "settings": {
            "domainStrategy": "UseIPv4"
        }
      },
      {
        "tag":"IP6_out", //IPv6优先
        "protocol": "freedom",
        "settings": {
          "domainStrategy": "UseIPv6"
        }
      },
      {
        "tag": "direct",  //自动选择
        "protocol": "freedom",
        "settings": {}
      },
      {
        "tag": "block", //封锁
        "protocol": "blackhole",
        "settings": {}
      },
      {
        "tag": "warp", //Cloudflare WARP 全局
        "protocol": "socks",
            "settings": {
                "servers": [{
                  "address": "127.0.0.1",
                  "port": 40000,
                  "users": []
                }]}
      },
      {
        "tag": "yto_out", //多伦多服务器出口
        "protocol": "trojan",
            "settings": {
              "servers": [
                {
                  "address": "***",
                  "port": 443,
                  "password": "***",
                  "flow": "xtls-rprx-direct-udp443",
                  "level": 0
                }
              ]
        }
    ],
    "routing": {
      "rules": [
        // IPv4
        {
          "type": "field",
          "outboundTag": "IP4_out",
          "domain": ["geosite:zoom"]
        },
     
        // IPv6
        {
            "type": "field",
            "outboundTag": "IP6_out",
            "domain": ["geosite:google","geosite:youtube","geosite:netflix"]
        },
     
        // Cloudflare Warp
        {
            "type": "field", // Social
            "outboundTag": "Warp",
            "domain": ["geosite:twitter","geosite:instagram","geosite:facebook","geosite:facebook-dev"]
        },
        {
          "type": "field", // Mastodon
          "outboundTag": "warp",
          "domain": ["domain:mastodon.social","domain:mstdn.social","domain:o3o.ca","domain:noc.social","domain:mstdn.ca"]
        },
        {
          "type": "field", // 中国大陆
          "outboundTag": "warp",
          "domain": ["geoip:cn"]
        },
        {
            "type": "field", // Archive
            "outboundTag": "warp",
            "domain": ["domain:archive.ph","domain:archive.today","domain:archive.org"]
        },
        
        // Auto
        {
          "type": "field", // IP Test
          "outboundTag": "direct",
          "domain": ["ip.sb","ipinfo.io"]
        },
        
        // ALL
        {
          "type": "field",
          "outboundTag": "direct",
          "network": "udp,tcp"
        },
        
        // Block
        {
            "type": "field", // 私网地址
            "ip": ["geoip:private"],
            "outboundTag": "block"
        }
      ]
    }
  }