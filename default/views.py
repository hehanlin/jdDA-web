from django.shortcuts import render, HttpResponse
import json
from .models import Category, GoodDetail, GoodDetailAnalysisResult
from random import choices
from scrapyd_api import ScrapydAPI
from base.settings import SCRAPYD_URL, SCRAPYD_PROJECT,GOOD_DETAIL_START_URL
import analysis.goodDetail
# Create your views here.


def index(request):
    return render(request, 'index.html')


def ping(request):
    return HttpResponse("1")


def category(request):
    all_three_cate = Category().get_category_three()
    res = choices(all_three_cate, k=50)
    return HttpResponse(json.dumps(res))


def search(request):
    keyword = request.GET.get("q", None)
    if not keyword:
        return HttpResponse(json.dumps([]))
    return HttpResponse(json.dumps(
        Category().search(keyword)
    ))


def good_list(request):
    cat_id = request.GET.get("cat_id", "9987,653,655")


def good_detail(request):
    good_id = request.GET.get("good_id", "6029342")
    good_ana_res = GoodDetailAnalysisResult().is_done(good_id)
    if not good_ana_res:
        good_info = GoodDetail().get(good_id)
        if not good_info:
            job_id = schedule_spider("goodDetail", start_url=GOOD_DETAIL_START_URL % good_id)
            return HttpResponse(job_id)
        else:
            analysis.goodDetail.main(good_id)
            return render(request, 'result.html')
    else:
        return render(request, 'result.html')


def good_ana_res(request):
    good_id = request.GET.get("good_id", "6029342")
    return HttpResponse(
        json.dumps(GoodDetailAnalysisResult().is_done(good_id), ensure_ascii=False)
    )


def schedule_spider(spider: str, **kwargs):
    scrapyd = ScrapydAPI(SCRAPYD_URL)
    job_id = scrapyd.schedule(SCRAPYD_PROJECT, spider, **kwargs)
    return job_id

