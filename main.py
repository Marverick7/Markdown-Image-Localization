#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import uuid
from shutil import copyfile

import requests


def get_files_list(target_dir):
    f_list = []
    top = os.path.abspath(target_dir)
    for root, dirs, files in os.walk(top, topdown=False):
        for file_name in files:
            file_name_split = file_name.split(".")
            if file_name_split[-1] == "md":
                md_file_path = os.path.join(root, ".".join(file_name_split))
                f_list.append(md_file_path)
    return f_list


def download_img(url, file):
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


def modify_url(file, flag):
    i = 0
    with open(file, "r", encoding="utf-8") as f1:
        data = f1.read()
        tmp = re.findall(r"!\[.*]\(.*\)", data, re.I | re.M)
        for url in tmp:
            url = re.findall(r"https?://[^\s]*\)", url)
            if url:
                i = i + 1
                url = url[0].rstrip(")")
                print(f"正在处理第{i}张图片")
                img_path = download_img(url, file)
                data = data.replace(url, img_path)
    if i != 0:
        if flag:
            copyfile(file, f"{file}.bak")
        with open(file, "w", encoding="utf-8") as f2:
            f2.write(data)
            print(f"处理完成，共处理{i}张图片")
            return True
    else:
        print("此文件没有需要处理的图片！")
        return False


def main_method(target_dir, flag):
    i = 0
    files_list = get_files_list(target_dir)
    for file in files_list:
        print("正在处理：" + file)
        if modify_url(file, flag):
            i = i + 1
    return len(files_list), i, len(files_list) - i


if __name__ == '__main__':
    print("是否备份原文件？（y or n）")
    while True:
        ipt = input().lower()
        if ipt == "y":
            backup = True
            break
        elif ipt == "n":
            backup = False
            break
        else:
            print("输入错误，请重新输入：")
    main_method("files", backup)
