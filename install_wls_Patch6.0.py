#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import sys
import subprocess
import datetime,time
import re
import commands


logname="/opt/wlspatch" + datetime.datetime.now().strftime("%Y%m%d%H%M%S")+"_log.txt"

##标记写入文件
def mark_file(filename,lx,str):
    f=open(filename,lx)
    nowtime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    f.write("[%s] %s \n" % (nowtime,str))
    f.close()

#函数1：检查weblogic Patch版本
def check_wlsPatch(wls_home,bsu_home):
 try:
    print(">>>>>>检查weblogic版本中...")
    mark_file(logname,'a',">>>>>>检查weblogic版本中...")
    check_cmd=('su - weblogic -c "cd %s;./bsu.sh -prod_dir=%s -status=applied -verbose -view|grep -E \'^Patch ID\'|cut -d \':\' -f 2|sed s/[[:space:]]//g|grep -v \')\'|tr -s \'\n\' \' \'"' % (bsu_home,wls_home))
    mark_file(logname,'a',">>>>>>>>当前执行命令:%s" % check_cmd)
    currentPatch =''.join(commands.getoutput(check_cmd)).replace('\n','')
    if currentPatch:
        print(">>>>>>当前weblogic Patch版本:%s" % currentPatch)
        mark_file(logname,'a',">>>>>>当前weblogic Patch版本:%s" % currentPatch)
    else:
        print(">>>>>>当前weblogic Patch版本: 无")
        mark_file(logname,'a',">>>>>>当前weblogic Patch版本:无")
    return currentPatch
 except subprocess.CalledProcessError as err:
      print err.output
      return err.returncode

#函数2：移除weblogic Patch版本
def remove_wlsPatch(wls_home,bsu_home,version):
 try:
    mark_file(logname,'a',">>>>>>>>移除版本前检查!!<<<<<<<<<<<<")
    print(">>>>>>>>移除版本前检查!!<<<<<<<<<<<<")
    currentPatch=check_wlsPatch(wls_home,bsu_home)
    plist=currentPatch.split()
    if currentPatch:
       if version=='1': 
          if len(plist)>1:
             plist.pop(0)
          else:
             print(">>>>>>当前系统Patch只有一个大版本，无Patch小版本，请选择mode为remove模式")
             mark_file(logname,'a',">>>>>>当前系统Patch只有一个大版本，无Patch小版本，请选择mode为remove模式")
             exit(0)
       for p in list(reversed(plist)):
           print(">>>>>>>>开始移除weblogic Patch版本：%s" % p)
           mark_file(logname,'a',">>>>>>>>开始移除weblogic Patch版本：%s" % p)
           check_cmd=('su - weblogic -c  "cd %s;./bsu.sh -remove -patchlist=%s -prod_dir=%s"'  % (bsu_home,p,wls_home))
           mark_file(logname,'a',">>>>>>>>当前执行命令:%s" % check_cmd)
           remove_str=commands.getoutput(check_cmd)
           print ">>>>>>>>移除进程:\n%s" % remove_str
           mark_file(logname,'a',">>>>>>>>移除进程:\n%s" % remove_str)
           print(">>>>>>>>移除weblogic Patch:%s 成功完成！！" % p)
           mark_file(logname,'a',">>>>>>>>移除weblogic Patch:%s 成功完成！！" % p)
       return 0
    else:
        print(">>>>>>>>当前没有可卸载的weblogic Patch版本，程序已经退出！！！")
        mark_file(logname,'a',">>>>>>>>当前没有可卸载的weblogic Patch版本，程序已经退出！！！")
        exit(0)
 except subprocess.CalledProcessError as err:
      print err.output
      return err.returncode

#函数3：安装weblogic Patch版本
def Install_wlsPatch(wls_home,bsu_home,New_wlsPatch,patch_file,version):
 try:
    mark_file(logname,'a',">>>>>>>>安装版本前检查!!<<<<<<<<<<<<")
    print(">>>>>>>>安装版本前检查!!<<<<<<<<<<<<")
    NewcurrentPatch=check_wlsPatch(wls_home,bsu_home)
    if NewcurrentPatch==New_wlsPatch:
       print(">>>>>>>>当前weblogic Patch已经是:%s 不需要再安装,程序已退出！！" % NewcurrentPatch)
       mark_file(logname,'a',">>>>>>>>当前weblogic Patch已经是:%s 不需要再安装,程序已退出！！" % NewcurrentPatch)
       exit(0)
    else:
        if version=='0':
           remove_wlsPatch(wls_home,bsu_home,version)
        try:
           unzip_cmd=("/usr/bin/unzip -o /opt/%s -d %s/cache_dir;chmod -R 777 %s/cache_dir" % (patch_file,bsu_home,bsu_home))
           print(">>>>>>>>当前执行解压命令:%s" % unzip_cmd)
           mark_file(logname,'a',">>>>>>>>当前执行解压命令:%s" % unzip_cmd)
           zxzt,output=commands.getstatusoutput(unzip_cmd)
           print(">>>>>>>>解压过程:\n%s" % output)
           mark_file(logname,'a',">>>>>>>>解压过程:\n%s" % output)
           if zxzt==0:
              print(">>>>>>>>解压weblogic Patch压缩包:%s 成功" % patch_file)
              mark_file(logname,'a',">>>>>>>>解压weblogic Patch压缩包:%s 成功" % patch_file)
           else:
              print(">>>>>>>>解压weblogic Patch压缩包:%s 失败" % patch_file)
              mark_file(logname,'a',">>>>>>>>解压weblogic Patch压缩包:%s 失败" % patch_file)
        except Exception as err:
           print(">>>>>>>>解压失败报错:%s" % ''.join(err))
           mark_file(logname,'a',''.join(err))
           exit(0)
        #print("开始停止weblogic所有服务！")
        #commands.getoutput("killall java")
        #print("weblogic所有服务停止完毕！")
        print(">>>>>>>>开始安装weblogic Patch版本：%s中..." % New_wlsPatch)
        mark_file(logname,'a',">>>>>>>>开始安装weblogic Patch版本：%s中..." % New_wlsPatch)
        check_cmd=('su - weblogic -c "cd %s;./bsu.sh -install -patch_download_dir=%s/cache_dir -patchlist=%s -prod_dir=%s"' % (bsu_home,bsu_home,New_wlsPatch,wls_home))
        mark_file(logname,'a',">>>>>>>>当前执行命令:%s" % check_cmd)
        install_str=commands.getoutput(check_cmd)
        print ">>>>>>>>安装进程:\n%s" % install_str
        mark_file(logname,'a',">>>>>>>>安装进程:\n%s" % install_str)
        NewcurrentPatch=check_wlsPatch(wls_home,bsu_home)
        if NewcurrentPatch==New_wlsPatch or New_wlsPatch in NewcurrentPatch:
            print(">>>>>>>>新的weblogic Patch:%s 安装成功！！" % NewcurrentPatch)
            mark_file(logname,'a',">>>>>>>>新的weblogic Patch:%s 安装成功！！" % NewcurrentPatch)
            return 0
        else:
            print(">>>>>>>>当前Weblogic Patch:%s 安装失败，请排查原因！！" % NewcurrentPatch)
            mark_file(logname,'a',">>>>>>>>当前Weblogic Patch:%s 安装失败，请排查原因！！" % NewcurrentPatch)
            exit(0)
 except subprocess.CalledProcessError as err:
    print err.output
    mark_file(logname,'a',">>>>>>>>当前Weblogic Install Patch,错误原因:%s" % err.output)
    return err.returncode

#函数四：更新weblogic Patch版本和安装Patch小版本
def Update_wlsPatch(wls_home,bsu_home,New_wlsPatch,patch_file,version):
 try:
    mark_file(logname,'a',">>>>>>>>更新版本前检查!!<<<<<<<<<<<<")
    print(">>>>>>>>更新版本前检查!!<<<<<<<<<<<<<<<")
    current_wlsVersion=check_wlsPatch(wls_home,bsu_home)
    patchcount=int(len(current_wlsVersion.split()))
    if current_wlsVersion:
        if current_wlsVersion == New_wlsPatch:
           mark_file(logname,'a',">>>>>>>>当前已经是最新版本:%s,程序退出！！"  % New_wlsPatch)
           print(">>>>>>>>当前已经是最新版本：%s" % New_wlsPatch)
           exit(0)
        else:
           if patchcount>=2 or version==0:
              remove_wlsPatch(wls_home,bsu_home,version)
           else:
              mark_file(logname,'a',">>>>>>>>当前安装Patch小版本，跳过卸载程序！")
              print(">>>>>>>>当前安装Patch小版本，跳过卸载程序！")
           Install_wlsPatch(wls_home,bsu_home,New_wlsPatch,patch_file,version)
           mark_file(logname,'a',">>>>>>>>安装版本后检查!!<<<<<<<<<<<<")
           print(">>>>>>>>安装版本后检查!!<<<<<<<<<<<<")
           current_wlsVersion=check_wlsPatch(wls_home,bsu_home)
    else:
        print(">>>>>>>>weblogic Patch版本：无 ,马上执行安装最新版本：%s" % New_wlsPatch)
        mark_file(logname,'a',">>>>>>>>weblogic Patch版本：无 ,马上执行安装最新版本：%s" % New_wlsPatch)
        Install_wlsPatch(wls_home,bsu_home,New_wlsPatch,patch_file,version)
    print(">>>>>>>>weblogic Patch %s 版本升级成功!!" % current_wlsVersion)
    mark_file(logname,'a',">>>>>>>>weblogic Patch %s 版本升级成功!!" % current_wlsVersion)
    return 0
 except subprocess.CalledProcessError as err:
      print err.output
      mark_file(logname,'a',">>>>>>>>当前Weblogic Update Patch,错误原因:%s" % err.output)
      return err.returncode

#1、通过进程获取WLS_HOME和BSU_HOME
def getProcessWLSArgs():
    # 获取wls_home
    mark_file(logname,'a',">>>>>>>>自动通过java进程获取【wls_home】和【bsu_home】中....")
    args=[]
    cmdInfo = "ps -eo command|grep java|grep -v grep|sed -n '1p'"
    cmd_output=''.join(commands.getoutput(cmdInfo)).replace('\n','')
    if cmd_output:
        temp = [block for block in cmd_output.split(" ") if "Dplatform.home" in block]
        wls_home = ''.join(temp).split('=')[1]
        # 获取bsu_home
        bsu_home = re.sub('wlserver_[0-9]+.*', 'utils/bsu', wls_home)
        args.extend([wls_home,bsu_home])
        return args
    else:
        print(">>>>>>>>检测服务异常:服务器无java进程,可能服务没有启动!!!")
        mark_file(logname,'a',">>>>>>>>您选择auto模式，但检测服务无java进程，请启动服务或选择手动模式")
        exit(0)
#2、检测目录和补丁包是否存在以及bsu内存大小检测，不符合就修改
def check_wls_env(wls_home,bsu_home,patch_file):
    mark_file(logname,'a',">>>>>>>>检查wls_home和bsu_home目录是否存在")
    if  not os.path.exists(wls_home):
       print(">>>>>>>>检测wls_home:%s目录不存在,请检查." %  wls_home)
       mark_file(logname,'a',">>>>>>>>检测wls_home:%s目录不存在,请检查." %  wls_home)
       exit(0)
    if  not os.path.exists(bsu_home):
       print(">>>>>>>>检测bsu_home:%s目录不存在,请检查." %  bsu_home)
       mark_file(logname,'a',">>>>>>>>检测wls_home:%s目录不存在,请检查." %  bsu_home)
       exit(0)
    package_path="/opt/%s" % patch_file
    if  not os.path.exists(package_path):
       print(">>>>>>>>检测patch_file:/opt目录下没有找到对应补丁包%s,请把补丁压缩包放在/opt目录下" %  patch_file)
       mark_file(logname,'a',">>>>>>>>检测patch_file:/opt目录下没有找到对应补丁包%s,请把补丁压缩包放在/opt目录下" %  patch_file)
       exit(0)
    print(">>>>>>>>wls_home、bsu_home目录和patch_file文件都检测成功")
    mark_file(logname,'a',">>>>>>>>wls_home、bsu_home目录和patch_file文件都检测成功")
    mark_file(logname,'a',">>>>>>>>成功获取wls_home:%s" % wls_home)
    mark_file(logname,'a',">>>>>>>>成功获取bsu_home:%s" % bsu_home)
    mark_file(logname,'a',">>>>>>>>成功获取package_path:%s" % package_path)
    print(">>>>>>>>成功获取wls_home:%s" % wls_home)
    print(">>>>>>>>成功获取bsu_home:%s" % bsu_home)
    print(">>>>>>>>成功获取package_path:%s" % package_path)
    #判断bsu mem是否是4096MB
    mark_file(logname,'a',">>>>>>>>检查bsu mem 值是否为4096MB....")
    check_cmd = ("cat %s/bsu.sh|grep MEM_ARGS=" % bsu_home)
    mem_value = re.sub("\D", "", ''.join(commands.getoutput(check_cmd)).split('-')[-1])
    mark_file(logname,'a',">>>>>>>>当前bsu mem值:%s " % mem_value)
    if mem_value != '4096':
       commands.getoutput(("sed -i 's@MEM_ARGS=.*@MEM_ARGS=\"-Xms4096m -Xmx4096m\"@'  %s/bsu.sh" % bsu_home))
       print(">>>>>>>>检测bsu内存为%sMB 修改为4096MB" % mem_value)
       mark_file(logname,'a',">>>>>>>>修改bsu mem值为4096MB")
    return 0

#帮助提示信息
def wls_help(scriptsName):
    print ('''
              --------------------------------------------------欢迎使用weblogic WLS Patch脚本（created by yulei）---------------------------------------------------------------------
              注意事项：安装之前请把补丁包，放在/opt目录下(输出日志放在/opt/wlspatchxxxxxxxx_log.txt),使用命令格式如下
              python %s [oper][mode] [wls_home] [bsu_home]
                                       --help  :  使用命令帮助
                                       --check :  检查weblogic Patch版本 
                                       --remove:  依次卸载当前weblogic Patch所有版本   
                                       --remove_version:  卸载当前weblogic Patch小版本   
                                       --install  [..] [新补丁名] [新wls包名]  :安装weblogic Patch版本                (前提是卸载之前的版本)
                                       --install_version  [..] [新补丁名] [新wls包名]  :安装weblogic Patch小版本        (保留之前的Patch大版本，安装所依赖的Patch小版本)
                                       --update   [..] [新补丁名] [新wls包名] :更新weblogic Patch版本 
                                       --update_version   [..] [新补丁名] [新wls包名] :用于升级Patch小版本,不用卸载之前存在的Patch版本 
                        其中oper{hand:手动指定目录,auto:自动通过启动java进程获取目录,其中前提是启动好服务的};
                        例如：(自动更新：weblogic最新漏洞补丁：python %s auto --update U5I2 p29204678_1036_Generic.zip)
                              (手动更新: weblogic最新漏洞补丁：python %s hand --update '/u01/middleware/wlserver_10.3' '/u01/middleware/utils/bsu' U5I2 p29204678_1036_Generic.zip )  
                              (自动更新小版本: weblogic最新漏洞补丁小版本：python %s auto --update_version  6JJ4 p29694149_10360190416_Generic.zip )  
                              (手动更新小版本: weblogic最新漏洞补丁小版本：python %s hand --update_version '/u01/middleware/wlserver_10.3' '/u01/middleware/utils/bsu' 6JJ4 p29694149_10360190416_Generic.zip)
             -----------------------------------------------------------------------------------------------------------------------------------------------------------------------          
          ''' % (scriptsName,scriptsName,scriptsName,scriptsName,scriptsName))
def main():
    mark_file(logname,'w',"**********************************************************Weblogic Patch版本修复报告*****************************************************************")
    mark_file(logname,'a',"修复时间：%s                                                                                 " % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    modes=['--help','--check','--update','--remove','--install','--update_version','--remove_version','--install_version']
    wls_home=''
    bsu_home=''
    New_wlsPatch=''
    patch_file=''
    wlsargs=sys.argv
    scriptsName=wlsargs[0]
    try:
        oper=wlsargs[1]
    except Exception:
        oper=''
    if oper!='auto' and oper !='hand':
       wls_help(scriptsName)
       exit(0)
    try:
        mode=wlsargs[2]
    except Exception:
        mode=''
    if mode not in modes:
        wls_help(scriptsName)
        exit(0)
    if oper=='auto':
       print(">>>>>>>>您选择:auto(自动模式).")
       mark_file(logname,'a',">>>>>>>>您选择:auto(自动模式).")
       try:
          New_wlsPatch=wlsargs[3]
       except Exception:
          New_wlsPatch=''
       try:
          patch_file=wlsargs[4]
       except Exception:
          patch_file=''
       wls_processargs=getProcessWLSArgs()
       wls_home=wls_processargs[0]
       bsu_home=wls_processargs[1]
    elif oper=='hand':
         print(">>>>>>>您选择:hand(手动模式).")
         mark_file(logname,'a',">>>>>>>您选择:hand(手动模式).")
         wls_home=wlsargs[3]
         bsu_home=wlsargs[4]
         try:
            New_wlsPatch=wlsargs[5]
         except Exception:
            New_wlsPatch=''
         try:
            patch_file=wlsargs[6]
         except Exception:
            patch_file=''
    check_wls_env(wls_home,bsu_home,patch_file)
    version='0'
    if mode==modes[7]:
       if New_wlsPatch=='' or patch_file=='':
          print(">>>>>>>>您没有输入[新补丁名]或[新wls包名],请按如下命令格式执行......")
          mark_file(logname,'a',">>>>>>>>您没有输入[新补丁名]或[新wls包名],请按如下命令格式执行......")
          wls_help(scriptsName)
          exit(0)
       else:
          print(">>>>>>>>您选择【InstallVersion wlsPatch】功能")
          mark_file(logname,'a',">>>>>>>>您选择【InstallVersion wlsPatch】功能")
          version='1'
          Install_wlsPatch(wls_home,bsu_home,New_wlsPatch,patch_file,version)
          exit(0)
    elif mode==modes[6]:
         print(">>>>>>>>您选择【RemoveVersion wlsPatch】功能")
         mark_file(logname,'a',">>>>>>>>您选择【RemoveVersion wlsPatch】功能")
         version='1'
         remove_wlsPatch(wls_home,bsu_home,version)
         exit(0)
    elif mode==modes[5]:
       if New_wlsPatch=='' or patch_file=='':
          print(">>>>>>>>您没有输入[新补丁名]或[新wls包名],请按如下命令格式执行......")
          mark_file(logname,'a',">>>>>>>>您没有输入[新补丁名]或[新wls包名],请按如下命令格式执行......")
          wls_help(scriptsName)
          exit(0)
       else:
          print(">>>>>>>>您选择【UpdateVersion wlsPatch】功能")
          mark_file(logname,'a',">>>>>>>>您选择【UpdateVersion wlsPatch】功能")
          version='1'
          Update_wlsPatch(wls_home,bsu_home,New_wlsPatch,patch_file,version)
    elif mode==modes[4]:
       print(">>>>>>>>您选择【Install wlsPatch】功能")
       mark_file(logname,'a',">>>>>>>>您选择【Install wlsPatch】功能")
       if New_wlsPatch=='' or patch_file=='':
          print(">>>>>>>>您没有输入[新补丁名]或[新wls包名],请按如下命令格式执行......")
          mark_file(logname,'a',">>>>>>>>您没有输入[新补丁名]或[新wls包名],请按如下命令格式执行......")
          wls_help(scriptsName)
          exit(0)
       else:
          version='0'
          Install_wlsPatch(wls_home,bsu_home,New_wlsPatch,patch_file,version)
          print(">>>>>>>>您选择【Install wlsPatch】功能")
          mark_file(logname,'a',">>>>>>>>您选择【Install wlsPatch】功能")
          exit(0)
    elif mode==modes[3]:
         print(">>>>>>>>您选择【Remove wlsPatch】功能")
         mark_file(logname,'a',">>>>>>>>您选择【Remove wlsPatch】功能")
         version='0'
         remove_wlsPatch(wls_home,bsu_home,version)
         exit(0)
    elif mode==modes[2]:
         if New_wlsPatch=='' or patch_file=='':
            print(">>>>>>>>您没有输入[新补丁名]或[新wls包名],请按如下命令格式执行......")
            mark_file(logname,'a',">>>>>>>>您没有输入[新补丁名]或[新wls包名],请按如下命令格式执行......")
            wls_help(scriptsName)
            exit(0)
         else:
            print(">>>>>>>>您选择【Update wlsPatch】功能")
            mark_file(logname,'a',">>>>>>>>您选择【Update wlsPatch】功能")
            version='0'
            Update_wlsPatch(wls_home,bsu_home,New_wlsPatch,patch_file,version)
            exit(0)
    elif mode==modes[1]:
        print(">>>>>>>>您选择【check wlsPatch】功能")
        mark_file(logname,'a',">>>>>>>>您选择【check wlsPatch】功能")
        check_wlsPatch(wls_home,bsu_home)
        exit(0)
    elif mode==modes[0]:
        print(">>>>>>>>您选择【wlsPatch help】功能")
        mark_file(logname,'a',">>>>>>>>您选择【wlsPatch help】功能")
        wls_help(scriptsName)
        exit(0)
    else:
        print(">>>>>>>>您选择【wlsPatch help】功能")
        mark_file(logname,'a',">>>>>>>>您选择【wlsPatch help】功能")
        wls_help(scriptsName)
        exit(0)



#main
if __name__ == '__main__':
    main()



