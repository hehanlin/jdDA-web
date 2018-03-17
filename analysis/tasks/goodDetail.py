# -*- coding: utf-8 -*-

from analysis.celery_app import celery_app
import re
import pandas as pd
import jieba
from collections import Counter
from default.models import GoodDetail as Model

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
        except:
            pass
        try:
            self.d['poor_top_nice_comment'], self.d['poor_top_nice_comment'] = self.get_top_comment(poor_comment)
        except:
            pass
        try:
            self.d['img_top_nice_comment'], self.d['img_top_nice_comment'] = self.get_top_comment(img_comment)
        except:
            pass
        try:
            self.d['after_top_nice_comment'], self.d['after_top_nice_comment'] = self.get_top_comment(after_comment)
        except:
            pass
        try:
            self.d['general_top_nice_comment'], self.d['general_top_nice_comment'] = self.get_top_comment(general_comment)
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
        del comment['creationTime']
        return comment

    def get_keyword_count(self, df: pd.DataFrame):
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
        nice_max = df.sort_values(['usefulVoteCount'], ascending=False).head(1)     # 点赞最高
        reply_max = df.sort_values(['replyCount'], ascending=False).head(1)     # 回复最多
        return nice_max, reply_max

def main(good_id=None):
    print(GoodDetail(Model().get(good_id or '6029342')))


if __name__ == '__main__':
    main()