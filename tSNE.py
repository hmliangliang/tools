# -*-coding: utf-8 -*-
# @Time    : 2024/9/11 16:04
# @File    : tSNE.py
# @Software: PyCharm

import datetime
import os
import argparse
import time
os.system("pip install fitsne")
import pandas as pd
from sklearn.manifold import TSNE


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_output', help='Output file path', type=str, default='')
    parser.add_argument('--data_input', help='map_feature_file', type=str, default='')
    parser.add_argument('--dim', help='前dim列表示ID', type=int, default=2)
    parser.add_argument('--n_components', help='数据降维的维数', type=int, default=2)
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
            data = pd.read_csv(os.path.join(path, file), sep=',', header=None).astype(object)
        else:
            data = pd.concat([data, pd.read_csv(os.path.join(path, file), sep=',', header=None).astype(object)], axis=0)
    tsne = TSNE(n_components=args.n_components, random_state=42)
    X_tsne = tsne.fit_transform(data.iloc[:, args.dim::])
    # 写入数据
    starttime = time.time()
    data = pd.concat([data.iloc[:, 0:args.dim], pd.DataFrame(X_tsne)], axis=1)
    data.to_csv(os.path.join(args.data_output, 'output.csv'), index=False, header=False, sep=',')
    endtime = time.time()
    print("文件写入完成，耗时:{} {}".format(endtime - starttime, datetime.datetime.now()))
