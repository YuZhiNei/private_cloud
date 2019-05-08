from django.shortcuts import render, redirect, reverse
# Django 给我们的试图类
from django.views.generic import View
# 导入 model
from .models import Upload, User
import random
import string
import json
from django.http import HttpResponsePermanentRedirect, HttpResponse


# 登录
class LoginView(View):

    def get(self, request):

        return render(request, 'login.html')

    def post(self, request):

        username = request.POST.get('username')
        password = request.POST.get('username')
        # 校验用户和密码
        users = User.objects.filter(username=username, password=password)
        if users.exists():
            # 设置 session
            request.session['username'] = username
            # 登录成功跳转到 home
            return redirect(reverse('home'))
        else:

            return HttpResponse('用户名或密码错误')


# 首页上传页面
class HomeView(View):

    # 首页 home，专门用于处理 get 请求
    def get(self, request):

        username = request.session.get('username', '')
        # 判断是否已经登录
        if not username:
            return redirect(reverse('login'))
            # return redirect(reverse('home.html'))
        return render(request, 'home.html')

    # post 请求
    def post(self,request):
        # 如果有文件
        if request.FILES:
            # 获取文件
            file = request.FILES.get('file')
            # 获取文件名
            name = file.name
            # 获取文件大小
            size = round(int(file.size) / 1024)
            # 写文件到 /static/files
            with open('static/file/' + name, 'wb') as f:
                f.write(file.read())
                # 随机生成 8 位 code
            code = ''.join(random.sample(string.digits, 8))
            username = request.session.get('username', '')
            user = User.objects.get(username=username)
            ids = user.id
            con = Upload(
                path='static/file/' + name,
                name=name,
                Filesize=size,
                code=code,
                # 获取上传文件的用户IP
                PCIP=str(request.META['REMOTE_ADDR']),
                user_id=ids
            )
            # 储存到数据库
            con.save()
            # 使用 HttpResponsePermanentRedirect 重定向到展示文件的页面
            return HttpResponsePermanentRedirect('/s/'+code)


# 展示文件的视图类
class DisplayView(View):
    # 支持 get 请求，并且可接受一个参数，这里的 code 需要和配置路由的 code 保持一致
    def get(self, request, code):
        # 以 code 查找
        con = Upload.objects.filter(code=str(code))
        # 如果 con 有内容，con 的访问次数 +1，否则返回给前端的内容也是空的
        if con:
            # 拿取数据字段
            for i in con:
                # 访问次数 +1
                i.DownloadDocount += 1
                # 保存
                i.save()
        # 返回页面，其中 content 是我们传给前端的内容
        return render(request, 'content.html', {"content": con})


# 定义一个 MyView 用于完成用户管理功能
class MyView(View):

    def get(self, request):

        username = request.session.get('username', '')
        if not username:
            return redirect(reverse('login'))
        user = User.objects.get(username=username)
        ids = user.id
        # 获取用户 IP
        # ip = request.META['REMOTE_ADDR']
        # 通过用户 IP 查找数据
        u = Upload.objects.filter(user_id=ids)
        for i in u:
            # 访问量 +1
            i.DownloadDocount += 1
            # 保存访问量
            i.save()
        return render(request, 'content.html', {'content': u})


# 搜索文件视图
class SearchView(View):
    def get(self, request):
        # 获取 get 请求中的 kw 值
        code = request.GET.get('kw')
        u = Upload.objects.filter(name=str(code))
        # 查询到的结果放到字典中
        data = {}
        if u:
            for i in range(len(u)):
                u[i].DownloadDocount += 1
                u[i].save()
                data[i] = {}
                data[i]['download'] = u[i].DownloadDocount
                data[i]['filename'] = u[i].name
                data[i]['id'] = u[i].id
                data[i]['ip'] = str(u[i].PCIP)
                data[i]['size'] = u[i].Filesize
                data[i]['time'] = u[i].Datatime
                data[i]['key'] = u[i].code
        return HttpResponse(json.dumps(data), content_type='application/json')