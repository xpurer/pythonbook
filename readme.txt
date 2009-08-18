环境配置

下载安装
http://www.python.org/ftp/python/2.6/python-2.6.msi
http://www.technicalbard.com/files/MySQL-python-1.2.2.win32-py2.6.exe


下载运行
http://peak.telecommunity.com/dist/ez_setup.py

添加
C:\Python26\Scripts
到环境变量 PATH


进入命令行，复制粘贴以下命令（可以一次性复制进去）
easy_install -U mako

运行build.py，可以编译文本

文本放在book下面

文本格式

小标题：
    == 这是h2 ==
    === 这是h3 ===

加粗:
    [[大规模]]减持美国国债

代码：
    {{{
    select * from user limit 100;
    delete from user where user_id = 1;
    }}}

图片:
    放到img目录,用png格式
    文中引用如
    
    测试用图 xxx.png

