# -*- coding: utf-8 -*-

import pandas as pd
from default.models import GoodList as Model, GoodListAnalysisResult as ResModel


class GoodList(object):
    """
    商品列表分析
    """
    def __init__(self, document):
        self.d = dict()
        self.d['id'] = document.get("_id")
        self.d['name'] = document.get("name", "未找到列表名称")
        self.d['good_num'] = document.get("good_num", "未找到商品总数")
        self.d['brand_list'] = document.get("brand_list", [])
        self.top_goods_df = pd.DataFrame(document['top_good_list'])
        self.d['title'] = self.top_goods_df['title'].tolist()
        self.top_goods_df['commit_num'] = self.top_goods_df['commit_num'].apply(self.replace_commit_num)
        self.d['commit_num'] = self.top_goods_df['commit_num'].tolist()
        self.top_goods_df['price'] = self.top_goods_df['price'].fillna(0).astype(float)
        self.d['price'] = self.top_goods_df['price'].tolist()
        self.top_goods_df['total_price'] = self.top_goods_df['commit_num'] * self.top_goods_df['price']
        self.d['total_price'] = self.top_goods_df['total_price'].tolist()
        shop_total = self.top_goods_df['total_price'].groupby(self.top_goods_df['shop_name']).sum()
        self.d['shop_total'] = shop_total.to_dict()
        shop_commit = self.top_goods_df['commit_num'].groupby(self.top_goods_df['shop_name']).sum()
        self.d['shop_commit'] = shop_commit.to_dict()

    @staticmethod
    def replace_commit_num(x: str):
        if x.find("万") != -1:
            tmp = x.replace("万", "").replace("+", "")
            tmp = float(tmp) * 10000
        elif x.find("+") != -1:
            tmp = x.replace("+", "")
            tmp = float(tmp)
        else:
            tmp = float(x)
        return tmp


def main(cat_id):
    res = GoodList(Model().get(cat_id)).d
    res['_id'] = cat_id
    ResModel().save(res)


if __name__ == "__main__":
    import sys, os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    main("9987,653,655")
