from turtle import pos
from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from .models import blogPost
# Create your views here.
def index(request):
    myposts = blogPost.objects.all()
    return render(request,'blog/index.html',{'myposts':myposts})
def blogpost(request,id):
    status1 = ""
    status2 = ""
    post = blogPost.objects.filter(post_id=id)
    prev = blogPost.objects.filter(post_id=id-1)
    next = blogPost.objects.filter(post_id=id+1)
    if len(prev)==0:
        status1 = "disabled"
    if len(next)==0:
        status2 = "disabled"
    return render(request,'blog/blogpost.html',{'post':post,'prev':prev,'next':next,'status1':status1,'status2':status2,'previd':id-1,'nextid':id+1})