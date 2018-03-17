from django.shortcuts import render, HttpResponse
import json
from .models import Category
from random import choices
# Create your views here.


def index(request):
    return render(request, 'index.html')


def ping(request):
    return HttpResponse("1")


def category(request):
    all_three_cate = Category().get_category_three()
    res = choices(all_three_cate, k=50)
    print(res)
    return HttpResponse(json.dumps(res))


def analysis_good_list(request):
    cat_id = request.GET.get("cat_id", "9987,653,655")


