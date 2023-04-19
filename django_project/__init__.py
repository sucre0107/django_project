import pymysql
pymysql.version_info=(1,3,13,"final",0)
pymysql.install_as_MySQLdb()
# 这一行代码必须放在这里，否则会报错
# 因为django在启动的时候会去读取这个文件，所以这个文件必须在django启动之前就已经存在
# 他的作用是将pymysql替换为MySQLdb，这样django就可以使用pymysql来连接mysql数据库了