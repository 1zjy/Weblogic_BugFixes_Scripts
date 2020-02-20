### 一、升级脚本说明

> <u>安装之前请把补丁包，放在/opt目录下</u>，具体使用命令格式如下 

```
python [最新脚本] [oper] [mode] [wls_home] [bsu_home]
                        --help  :  使用命令帮助
                        --check :  检查weblogic Patch版本 
                        --remove:  依次卸载当前weblogic Patch所有版本   
                        --remove_version: 卸载当前weblogic Patch小版本   
                        --install  [..][新补丁名] [新wls包名]:卸载原大版本,安装Patch大版本 
                        --install_version [..][新补丁名] [新wls包名]:安装Patch小版本,保留大版本 
                        --update   [..] [新补丁名] [新wls包名] :更新Patch大版本，包括卸载和安装 
                        --update_version[..] [新补丁名] [新wls包名] :更新Patch小版本,保留大版本                             
 [oper]hand: 【手动模式】手工指定[wls_home]和[bsu_home]目录；
 [oper]auto: 【自动模式】自动通过weblogic进程获取目录[wls_home]和[bsu_home],前提条件：有服务运行;
 [..]: 为[wls_home]和[bsu_home]目录
 [新补丁名] : zip的压缩补丁包解压出来 XXX.jar文件或安装后版本检查XXX,补丁名就是XXX。
 [新wls包名]: 官网一般提供zip的压缩补丁包
```

> 注意事项：
>
> 【python版本】目前支持python2版本，python3还不支持
>
> 【root用户执行】执行脚本用户统一请用root用户执行，脚本会自动切换weblogic 用户执行操作。（如果用weblogic用户执行，脚本执行可能进入死循环）
>
> 【检查是否升级成功】请查看升级日志（/opt/wlspatchxxxxxxxx_log.txt）,来验证检查、移除、安装过程是否成功。

##### 常用操作格式举例：

```
2019年 weblogic:Path大版本为U5I2   Path小版本为IL49

------------------------大版本更新----------------------------
【自动更新大版本】：
python ./install_wls_Patch7.0.py auto --update U5I2 p29204678_1036_Generic.zip
【手动更新大版本】:
python ./install_wls_Patch7.0.py hand --update '/u01/middleware/wlserver_10.3' '/u01/middleware/utils/bsu' U5I2 p29204678_1036_Generic.zip 
------------------------小版本更新----------------------------
【自动更新小版本】:
python ./install_wls_Patch7.0.py auto --update_version  IL49 p29694149_10360190416_Generic.zip
【手动更新小版本】: 
python ./install_wls_Patch7.0.py hand --update_version '/u01/middleware/wlserver_10.3' '/u01/middleware/utils/bsu' IL49 p29694149_10360190416_Generic.zip

------------------------版本单独卸载------------------------
【自动卸载大小版本】python ./install_wls_Patch7.0.py auto --remove       //卸载U5I2和IL49
【自动卸载小版本】python ./install_wls_Patch7.0.py auto --remove_version  //只卸载IL49

2020年weblogic:path大版本：JWEB
【自动更新大版本】：
python ./install_wls_Patch7.0.py auto --update JWEB p29204678_1036_Generic.zip
```



