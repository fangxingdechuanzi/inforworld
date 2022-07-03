from django.shortcuts import render

# Create your views here.
#首页
def index_view(request):
    return render(request,'index/index.html')

def contact_views(request):
    return render(request, 'index/contact.html')
