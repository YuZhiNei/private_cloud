from django.db import models
from datetime import datetime


class User(models.Model):

    # 用户
    username = models.CharField(max_length=16, verbose_name='用户', unique=True)
    # 密码
    password = models.CharField(max_length=32, verbose_name='用户密码')

    class Meta:
        verbose_name = 'user'
        # 定义数据表名
        db_table = 'user'

    def __str__(self):

        return self.username

class Upload(models.Model):

    user = models.ForeignKey('User')
    # 访问该页面的次数, IntegerField 表示整数字段
    DownloadDocount = models.IntegerField(verbose_name='访问次数', default=0)
    # 唯一标识一个文件, CharField 表示字符串字段
    code = models.CharField(max_length=8, verbose_name='code')
    # Datatime 表示文件上传时间, datetime.new 不能加括号, 否则时间变成了表的生成时间
    Datatime = models.CharField(max_length=32, default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), verbose_name='添加时间')
    # path 表示文件储存的路径
    path = models.CharField(max_length=32, verbose_name='下载路径')
    # name 文件名
    name = models.CharField(max_length=32, verbose_name='文件名', default='')
    # Filesize 文件大小
    Filesize = models.CharField(max_length=10, verbose_name='文件大小')
    # PCIP 上传文件的IP
    PCIP = models.CharField(max_length=32, verbose_name='文件IP', default='')

    class Meta:

        verbose_name = 'download'
        # 定义数据表名
        db_table = 'download'

    def __str__(self):
        # 表示在做查询操作时，我们看到的是 name 字段
        return self.name

