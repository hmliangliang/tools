# -*-coding: utf-8 -*-
# @Time    : 2024/9/26 17:17
# @File    : padding.py
# @Software: PyCharm

import datetime
import os
import argparse
import time
import pandas as pd


def process_string(s):
    # 按逗号分割字符串
    elements = s.split(',')
    # 获取前args.start_num到args.end_num个元素
    first_10_elements = elements[0:args.max_length]
    # 如果元素不足args.str_num个，用'0'填充
    if len(first_10_elements) < args.max_length:
        first_10_elements.extend(['0'] * (args.max_length - len(first_10_elements)))
    # 用逗号拼接成字符串
    return ','.join(first_10_elements)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_output', help='Output file path', type=str, default='')
    parser.add_argument('--data_input', help='map_feature_file', type=str, default='')
    parser.add_argument('--max_length', help='最大的长度', type=int, default=1000)
    parser.add_argument('--col_num', help='处理的列数', type=int, default=8)
    parser.add_argument('--split_col', help='截取字符串所在列号(从0开始)', type=int, default=5)
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
        data = pd.read_csv(os.path.join(path, file), sep=';', header=None).astype(object)
        for i in range(args.split_col, args.split_col + args.col_num):
            data['new_column{}'.format(i)] = data[i].apply(process_string)
        # 写入数据
        start_time = time.time()
        data.to_csv(os.path.join(args.data_output, 'output_{}.csv'.format(count)), index=False, header=False, sep=';')
        end_time = time.time()
        print("第{}个文件写入完成，耗时:{} {}".format(count, end_time - start_time, datetime.datetime.now()))
