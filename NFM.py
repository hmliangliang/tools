# -*-coding: utf-8 -*-
# @Time    : 2024/9/6 11:03
# @File    : NFM.py
# @Software: PyCharm

import datetime
import os
import argparse
import time

import numpy as np
import pandas as pd
from sklearn.decomposition import NMF

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_output', help='Output file path', type=str, default='')
    parser.add_argument('--data_input', help='map_feature_file', type=str, default='')
    parser.add_argument('--n_components', help='非负矩阵分解n_components的数量', type=int, default=10)
    parser.add_argument('--dim', help='数据中非矩阵分解矩阵数据的维数', type=int, default=2)
    parser.add_argument('--tag', help='返回信息(all: 全部矩阵 user: 用户矩阵 item:商品矩阵)', type=str, default="item")
    parser.add_argument("--tb_log_dir", help="日志位置", type=str, default='')
    args = parser.parse_args()
    # 读取数据
    path = args.data_input.split(',')[0]
    input_files = sorted([file for file in os.listdir(path) if file.find("part-") != -1])
    n_files = len(input_files)
    count = 0
    for file in input_files:
        count += 1
        print("一共{}个文件,当前正在处理第{}个文件,文件路径:{}......".format(n_files, count,
                                                                             "cfs://" + path + "/" + file))
        # 读取数据数据最后一列为序列数据
        if count == 1:
            data = pd.read_csv(os.path.join(path, file), sep=';', header=None).astype(object)
        else:
            data = pd.concat([data, pd.read_csv(os.path.join(path, file), sep=';', header=None).astype(object)], axis=0)

    nmf_model = NMF(n_components=args.n_components, init='random', random_state=42)
    if args.tag == "all":
        W = nmf_model.fit_transform(data.iloc[:, args.dim::].astype(np.float))  # 用户特征矩阵
        H = nmf_model.components_  # 物品特征矩阵
        W = pd.DataFrame(W)
        H = pd.DataFrame(H)
    elif args.tag == "user":
        W = nmf_model.fit_transform(data.iloc[:, args.dim::].astype(np.float))  # 用户特征矩阵
        # 写入数据
        starttime = time.time()
        W = pd.DataFrame(W)
        W.to_csv(os.path.join(args.data_output, 'output.csv'), index=False, header=False, sep=';')
        endtime = time.time()
        print("文件写入完成，耗时:{} {}".format(endtime - starttime, datetime.datetime.now()))
    else:
        nmf_model.fit_transform(data.iloc[:, args.dim::].astype(np.float))
        H = nmf_model.components_  # 物品特征矩阵
        # 写入数据
        starttime = time.time()
        H = pd.DataFrame(H)
        H.to_csv(os.path.join(args.data_output, 'output.csv'), index=False, header=False, sep=';')
        endtime = time.time()
        print("文件写入完成，耗时:{} {}".format(endtime - starttime, datetime.datetime.now()))


