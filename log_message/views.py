from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
# Create your views here.

#装饰器判断登录状态
def check_login(fn):
    def wrap(request, *args, **kwargs):
        if 'username' not in request.session or 'uid' not in request.session:
            c_username = request.COOKIES.get('username')
            c_uid = request.COOKIES.get('uid')
            if not c_username or not c_uid:
                return HttpResponseRedirect('/user/login/')
            else:
                request.session['username'] = c_username
                request.session['uid'] = c_uid
        return fn(request, *args, **kwargs)
    return wrap

#笔记列表
@check_login
def list_view(request):
    if request.method == 'GET':
        user_id = request.session['uid']
        all_note = Note.objects.filter(user_id=user_id).order_by('updated_time')
        return render(request, 'log_message/note_list.html', locals())

#添加笔记
#装饰器判断登录状态
@check_login
def add_note(request):
    if request.method == 'GET':
        return render(request, 'log_message/add_note.html')
    elif request.method == 'POST':
        uid = request.session['uid']
        title = request.POST['title']
        content = request.POST['content']
        Note.objects.create(title=title, content=content, user_id=uid)
        return HttpResponseRedirect('/note/')

#查看笔记
@check_login
def note_look(request,noteid):
    try:
        note = Note.objects.get(id=noteid)
        return render(request, 'log_message/look_note.html', locals())
    except:
        return HttpResponse('你的笔记不存在')

#删除笔记
@check_login
def del_note(request,noteid):
    try:
        note = Note.objects.get(id=noteid)
        note.delete()
        return HttpResponseRedirect('/note/')
    except:
        return HttpResponse('你的笔记不存在')

#更新笔记
@check_login
def update_note(request,noteid):
    try:
        note = Note.objects.get(id=noteid)
    except:
        return HttpResponse('你的笔记不存在')
    if request.method == 'GET':
        return render(request, 'log_message/update_note.html', locals())
    elif request.method == 'POST':
        note.title = request.POST.get('title')
        note.content = request.POST.get('content')
        note.save()
        return HttpResponseRedirect('/note/')
