# -*- coding: utf-8 -*-

from analysis.celery_app import celery_app
import re
import pandas as pd
import jieba
from collections import Counter
from default.models import GoodDetail as Model, GoodDetailAnalysisResult as ResModel

class GoodDetail(object):

    def __init__(self, document):
        self._document = document
        self.d = dict()
        self.d['name'] = self._document.get('name', '尚未找到商品名称')
        self.d['url'] = self._document.get('url', '尚未找到商品url')
        self.d['comment_count'] = self.set_comment_count()  # 评价总数
        self._cs_s = pd.Series(
            self._document.get('comment_desc')['productCommentSummary']
        )   # cs_s comment summary series
        self._cs_s['imageListCount'] = document.get('comment_desc')['imageListCount']
        self.d['official_comment_rate'] = self.set_official_comment_rate()  # 官方好评
        self.d['five_star_rate'] = self.set_five_star_rate()    # 五星好评率
        thousand_comment = self.get_comments_df('all_comments')
        tc_time_comments_size = thousand_comment.to_period("d").groupby(level=0).size()
        tc_time_comments_size.index = tc_time_comments_size.index.to_datetime().strftime("%Y-%m-%d")
        self.d['everyday_comment_size'] = tc_time_comments_size.to_dict()   # 每日评论数统计
        histogram_score = thousand_comment.groupby('score').size()
        histogram_score.index = ['1星', '2星', '3星', '4星', '5星']
        self.d['histogram_score'] = histogram_score.to_dict()   # 星级分布
        keyword_of_summary = document['comment_desc'].get('hotCommentTagStatistics')
        keyword_of_summary = pd.DataFrame(keyword_of_summary)[['name', 'count']]
        keyword_of_summary.index = keyword_of_summary['name']
        del keyword_of_summary['name']
        try:
            self.d['keyword_of_summary'] = keyword_of_summary.to_dict()['count']     # 官方关键字摘要
        except:
            pass
        try:
            self.d['thousand_keyword'] = self.get_keyword_count(thousand_comment)  # 前一千条关键字摘要
            general_comment = self.get_comments_df('general_comments')
            self.d['general_keyword'] = self.get_keyword_count(general_comment)     # 中评摘要
        except:
            pass
        try:
            poor_comment = self.get_comments_df('poor_comments')
            self.d['poor_keyword'] = self.get_keyword_count(poor_comment)       # 差评摘要
        except:
            pass
        try:
            img_comment = self.get_comments_df('poor_comments')
            self.d['img_keyword'] = self.get_keyword_count(img_comment)        # 有图摘要
        except:
            pass
        try:
            after_comment = self.get_comments_df('after_comments')
            self.d['after_comment'] = self.get_keyword_count(after_comment)     # 追评摘要
        except:
            pass
        try:
            self.d['all_top_nice_comment'], self.d['all_top_reply_comment'] = self.get_top_comment(thousand_comment)
        except Exception as e:
            print(e)
        try:
            self.d['poor_top_nice_comment'], self.d['poor_top_reply_comment'] = self.get_top_comment(poor_comment)
        except:
            pass
        try:
            self.d['img_top_nice_comment'], self.d['img_top_reply_comment'] = self.get_top_comment(img_comment)
        except:
            pass
        try:
            self.d['after_top_nice_comment'], self.d['after_top_reply_comment'] = self.get_top_comment(after_comment)
        except:
            pass
        try:
            self.d['general_top_nice_comment'], self.d['general_top_reply_comment'] = self.get_top_comment(general_comment)
        except:
            pass
        try:
            self.set_buy_channel(thousand_comment)
        except:
            pass
        try:
            self.set_buy_color(thousand_comment)
        except:
            pass
        try:
            self.set_buy_size(thousand_comment)
        except:
            pass
        try:
            self.set_buy_province(thousand_comment)
        except:
            pass
        try:
            self.set_buy_days(thousand_comment)
        except:
            pass
        try:
            self.set_user_level(thousand_comment)
        except:
            pass
        try:
            self.set_hour(thousand_comment)
        except:
            pass
        try:
            self.set_sell_time(thousand_comment)
        except:
            pass



    def set_comment_count(self):
        """
        商品评论数
        :return:
        """
        num = self._document.get('comment_count', None)
        if not num:
            return None
        reg = re.compile(r"(\d+)(万)?(\+)?")
        res = reg.search(num)
        if res and res.group(1):
            num = int(res.group(1))
            if res.group(2):
                num *= 10000
        return num

    def set_official_comment_rate(self):
        """
        官方好评（三星及以上），中评，　差评率, 数量
        :return:
        """
        official_comment_rate = self._cs_s[['goodCount', 'generalCount', 'poorCount', 'imageListCount', 'afterCount']]
        official_comment_rate.index = ['官方好评', '中评', '差评', '有图', '追评']
        return official_comment_rate.to_dict()

    def set_five_star_rate(self):
        """
        五星好评率
        :return:
        """
        return self._cs_s['defaultGoodCount']/self._cs_s['commentCount']

    def get_comments_df(self, s: str):
        comment = self._document.get(s)
        comment = pd.DataFrame(comment)
        comment.index = pd.to_datetime(comment['creationTime'])
        return comment

    def get_keyword_count(self, df: pd.DataFrame):
        """
        关键词摘要，生成词云
        :param df:
        :return:
        """
        comment_content = df['content']
        comment_content = "".join(comment_content)
        wordlist_after_jieba = jieba.cut(comment_content)
        wl_space_split = " ".join(wordlist_after_jieba)
        keyword_count = [each for each in wl_space_split.split() if len(each) > 1]
        keyword_count = Counter(keyword_count)
        keyword_count_s = pd.Series(keyword_count)
        keyword_count_s = keyword_count_s[keyword_count_s > 10]
        return keyword_count_s.to_dict()

    def get_top_comment(self, df: pd.DataFrame):
        """
        提取最受关注的评论
        :param df:
        :return:
        """
        nice_max = df.sort_values(
            ['usefulVoteCount'], ascending=False
        ).head(1)[['usefulVoteCount', 'content']].to_dict(orient='records')[0]   # 点赞最高
        reply_max = df.sort_values(
            ['replyCount'], ascending=False
        ).head(1)[['replyCount', 'content']].to_dict(orient='records')[0]    # 回复最多
        return nice_max, reply_max

    def set_buy_channel(self, df: pd.DataFrame):
        """
        购买渠道分析
        :param df:
        :return:
        """
        obj = df['userClientShow']
        obj = obj.value_counts()
        obj = obj.rename({'': '来自京东网页端'})
        self.d['buy_channel'] = obj.to_dict()
        obj = df['isMobile']
        obj = obj.value_counts()
        obj = obj.rename({1: '移动端', 0: 'PC'})
        self.d['is_mobile'] = obj.to_dict()

    def set_buy_color(self, df: pd.DataFrame):
        """
        购买属性分析
        :param df:
        :return:
        """
        obj = df['productColor']
        obj = obj.value_counts()
        self.d['buy_color'] = obj.to_dict()

    def set_buy_size(self, df: pd.DataFrame):
        """
        购买配置分析
        :param df:
        :return:
        """
        obj = df['productSize']
        obj = obj.value_counts()
        self.d['buy_size'] = obj.to_dict()

    def set_buy_province(self, df: pd.DataFrame):
        """
        购买者的地域分析
        :return:
        """
        obj = df['userProvince']
        obj = obj.value_counts()
        obj = obj.rename({"": "用户不授权地理位置"})
        self.d['buy_province'] = obj.to_dict()

    def set_buy_days(self, df: pd.DataFrame):
        """
        购买后的多少天评价
        :return:
        """
        obj = df['days'].value_counts().sort_index()
        if len(obj.index) > 20:
            value = obj[obj.index >= 20].sum()
            obj = obj.drop(obj[obj.index > 20].index)
            obj.values[-1] += value
        obj.index = [
            str(each) + "天" for each in obj.index
        ]
        obj = obj.rename({'0天': "当天"})
        if len(obj.index) > 20:
            obj = obj.rename({"20天": "20天后"})
        self.d['buy_days'] = obj.to_dict()

    def set_user_level(self, df: pd.DataFrame):
        """
        用户等级分析
        :param df:
        :return:
        """
        obj = df['userLevelName']
        obj = obj.value_counts()
        self.d['user_level'] = obj.to_dict()

    def set_hour(self, df: pd.DataFrame):
        """
        24小时分布
        :param df:
        :return:
        """
        obj = df['creationTime']
        obj = pd.DatetimeIndex(obj).hour.value_counts().sort_index()
        obj.index = [
            str(each) + "时" for each in obj.index
        ]
        self.d['comment_hour'] = obj.to_dict()      # 评论时间
        obj = df['referenceTime']
        obj = pd.DatetimeIndex(obj).hour.value_counts().sort_index()
        obj.index = [
            str(each) + "时" for each in obj.index
        ]
        self.d['buy_hour'] = obj.to_dict()      # 购买时间

    def set_sell_time(self, df: pd.DataFrame):
        """
        分析每月商品购买数量与评论数量
        :param df:
        :return:
        """
        obj = pd.Series(index=pd.DatetimeIndex(df['creationTime']), data=1)
        obj = obj.resample("M").sum().fillna(0)
        obj.index = obj.index.to_datetime().strftime("%Y-%m")
        self.d['sell_comment_month'] = obj.to_dict()     # 评论数量
        obj = pd.Series(index=pd.DatetimeIndex(df['referenceTime']), data=1)
        obj = obj.resample("M").sum().fillna(0)
        obj.index = obj.index.to_datetime().strftime("%Y-%m")
        self.d['sell_buy_month'] = obj.to_dict()        # 购买数量


def main(good_id):
    res = GoodDetail(Model().get(good_id)).d
    res['_id'] = good_id
    ResModel().save(res)


if __name__ == '__main__':
    main('6029342')