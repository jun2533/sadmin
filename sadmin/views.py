from django.shortcuts import render,render_to_response
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def index(request):
    return render(request,'app01/index.html')


def about(request):
    return render(request,'app01/about.html')