from django.shortcuts import render
from .models import Blogpost
from shop.models import ProjectSetting
# Create your views here.
from django.http import HttpResponse

def index(request):
    myposts = Blogpost.objects.all()
    setting = ProjectSetting.objects.get(id=1)
    params={
    'myposts':myposts,
    'setting':setting,
    }
    return render(request, 'blog/index.html',params)

def blogpost(request, id):
	post = Blogpost.objects.filter(post_id = id)[0]
	setting = ProjectSetting.objects.get(id=1)
	params={
    'post':post,
    'setting':setting,
    }
	return render(request, 'blog/blogpost.html',params)