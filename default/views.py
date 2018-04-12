from django.shortcuts import render, HttpResponse
import json
from .models import Category, GoodDetail, GoodDetailAnalysisResult, GoodListAnalysisResult, GoodList, SpiderTask
from random import choices
from scrapyd_api import ScrapydAPI
from base.settings import SCRAPYD_URL, SCRAPYD_PROJECT, GOOD_DETAIL_START_URL, GOOD_LIST_START_URL
import analysis.goodDetail, analysis.goodList
from time import sleep


# Create your views here.


def index(request):
    return render(request, 'index.html')


def ping(request):
    return HttpResponse("1")


def category(request):
    res = Category().get_category_three()
    return HttpResponse(json.dumps(res))


def search(request):
    keyword = request.GET.get("q", None)
    if not keyword:
        return HttpResponse(json.dumps([]))
    return HttpResponse(json.dumps(
        Category().search(keyword)
    ))


def top_ana_detail(request):
    return HttpResponse(json.dumps(
        GoodDetailAnalysisResult().get_top_ana()
    ))


def good_detail(request):
    good_id = request.GET.get("good_id", "6029342")
    good_ana_res = GoodDetailAnalysisResult().is_done(good_id)
    if not good_ana_res:
        good_info = GoodDetail().get(good_id)
        if not good_info:
            job_id = SpiderTask().get(good_id)
            if job_id:
                return HttpResponse("已存在当前任务，爬虫正在努力爬取中，请稍等片刻刷新重试!")
            job_id = schedule_spider("goodDetail", start_url=GOOD_DETAIL_START_URL % good_id)
            SpiderTask().save({"_id": good_id, "job_id": job_id})
            while True:
                status = status_spider(job_id)
                if status == "finished":
                    SpiderTask().delete(good_id)
                    break
                sleep(3)
            analysis.goodDetail.main(good_id)
            return render(request, 'result.html')
        else:
            analysis.goodDetail.main(good_id)
            return render(request, 'result.html')
    else:
        GoodDetailAnalysisResult().inc_hot(good_id)
        return render(request, 'result.html')


def good_list(request):
    cat_id = request.GET.get("cat_id", "9987,653,655")
    Category().inc_hot(cat_id)
    cat_ana_res = GoodListAnalysisResult().is_done(cat_id)
    if not cat_ana_res:
        cat_info = GoodList().get(cat_id)
        if not cat_info:
            job_id = SpiderTask().get(cat_id)
            if job_id:
                return HttpResponse("已存在当前任务，爬虫正在努力爬取中，请稍等片刻刷新重试!")
            job_id = schedule_spider("goodList", start_url=GOOD_LIST_START_URL % cat_id)
            SpiderTask().save({"_id": cat_id, "job_id": job_id})
            while True:
                status = status_spider(job_id)
                if status == "finished":
                    SpiderTask().delete(cat_id)
                    break
                sleep(3)
            analysis.goodList.main(cat_id)
            return render(request, 'good_list.html')
        else:
            analysis.goodList.main(cat_id)
            return render(request, 'good_list.html')
    else:
        return render(request, 'good_list.html')


def good_ana_res(request):
    good_id = request.GET.get("good_id", "6029342")
    return HttpResponse(
        json.dumps(GoodDetailAnalysisResult().is_done(good_id), ensure_ascii=False)
    )


def list_ana_res(request):
    cat_id = request.GET.get("cat_id", "9987,653,655")
    return HttpResponse(
        json.dumps(GoodListAnalysisResult().is_done(cat_id), ensure_ascii=False)
    )


def schedule_spider(spider: str, **kwargs):
    scrapyd = ScrapydAPI(SCRAPYD_URL)
    job_id = scrapyd.schedule(SCRAPYD_PROJECT, spider, **kwargs)
    return job_id


def status_spider(job_id):
    scrapyd = ScrapydAPI(SCRAPYD_URL)
    status = scrapyd.job_status(SCRAPYD_PROJECT, job_id)
    return status


