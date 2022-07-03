from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import User
import hashlib

# Create your views here.
#用户注册
def reg_view(request):
    if request.method == 'GET':
        return render(request, 'user/register.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password_1']
        password2 = request.POST['password_2']
        if password1 != password2:
            return HttpResponse('两次密码不一致')
        old_users = User.objects.filter(username=username)
        if old_users :
            return HttpResponse('用户名已注册')
        #哈希密码
        m = hashlib.md5()
        m.update(password1.encode())
        password_m = m.hexdigest()
        try:
            user = User.objects.create(username=username, password=password_m)
        except Exception as e:
            print('--create user error {}'.format(e))
            return HttpResponse('用户名已注册')
        #注册后免登录一天
        request.session['username'] = username
        request.session['uid'] = user.id
        #修改session存储时间
        return HttpResponseRedirect('/index')

#用户登录
def login_view(request):
    if request.method == 'GET':
        #检查登录状态
        if request.session.get('username') and request.session.get('uid'):
            return HttpResponseRedirect('/index')
        c_username = request.COOKIES.get('username')
        c_uid = request.COOKIES.get('uid')
        if c_username and c_uid:
            request.session['username'] = c_username
            request.session['uid'] = c_uid
            return HttpResponseRedirect('/index')
        return render(request, 'user/login.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
        except Exception as e:
            print('--login user error {}'.format(e))
            return HttpResponse('用户名或密码错误')

        m = hashlib.md5()
        m.update(password.encode())
        password_h = m.hexdigest()
        if password_h != user.password:
            return HttpResponse('用户名或密码错误')

        resp = HttpResponseRedirect('/index')
        request.session['username'] = username
        request.session['uid'] = user.id
        #记住用户
        if 'remember' in request.POST:
            resp.set_cookie('username', username, 3600*24*3)
            resp.set_cookie('uid', user.id, 3600*24*3)
        return resp

#退出登录
def logout_view(request):
    if 'username' in request.session:
        del request.session['username']
        # a=request.session['username']
        # del a
    if 'uid' in request.session:
        del request.session['uid']

    resp = HttpResponseRedirect('/index')
    if 'username' in request.COOKIES:
        resp.delete_cookie('username')
    if 'uid' in request.COOKIES:
        resp.delete_cookie('uid')
    return resp