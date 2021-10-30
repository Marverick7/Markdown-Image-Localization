#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import uuid

import requests


def get_files_list(t_dir):
    f_list = []
    top = os.path.abspath(t_dir)
    for root, dirs, files in os.walk(top, topdown=False):
        for file_name in files:
            file_name_split = file_name.split(".")
            if file_name_split[-1] == "md":
                md_file_path = os.path.join(root, ".".join(file_name_split))
                f_list.append(md_file_path)
    return f_list


def download_img(url):
    img_data = requests.get(url).content
    filename = os.path.basename(file)
    dirname = os.path.dirname(file)
    output_dir = os.path.join(dirname, f"{filename}.assets")
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    img_path = os.path.join(output_dir, f"{uuid.uuid4().hex}.jpg")
    with open(img_path, "wb+") as f:
        f.write(img_data)
    return img_path


def modify_url(t_file):
    i = 0
    with open(t_file, "r", encoding="utf-8") as f1, open(f"{t_file}.bak", "w", encoding="utf-8") as f2:
        data = f1.read()
        tmp = re.findall(r"!\[.*]\(.*\)", data, re.I | re.M)
        for url in tmp:
            url = re.findall(r"https?://[^\s]*\)", url)
            if url:
                i = i + 1
                url = url[0].rstrip(")")
                print(f"正在处理第{i}张图片")
                img_path = download_img(url)
                data = data.replace(url, img_path)
        if i != 0:
            f2.write(data)
            print(f"处理完成，共处理{i}张图片")
    if i != 0:
        os.remove(t_file)
        os.rename(f"{t_file}.bak", t_file)
    else:
        print("此文件没有需要处理的图片！")
        os.remove(f"{t_file}.bak")


if __name__ == '__main__':
    # 将target_dir修改为存放md文件的目录
    target_dir = "files"
    files_list = get_files_list(target_dir)

    for file in files_list:
        print("正在处理：" + file)
        modify_url(file)