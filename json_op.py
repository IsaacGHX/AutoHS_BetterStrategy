import sys
import requests
import json
import os
from datetime import datetime
from autohs_logger import *

# 来源于互联网的炉石JSON数据下载API, 更多信息可以访问 https://hearthstonejson.com/
def download_json(json_path):
    json_url = "https://api.hearthstonejson.com/v1/latest/zhCN/cards.json"
    file = requests.get(json_url)

    with open(json_path, "wb") as f:
        f.write(file.content)


def read_json(re_download=False):
    logger.info("正在读取cards.json文件")
    dir_path = os.path.dirname(__file__)
    if dir_path == "":
        dir_path = "."
    json_path = dir_path + "/cards.json"

    if not os.path.exists(json_path):
        logger.info("未找到cards.json,试图通过网络下载文件")
        try:
            download_json(json_path)
            logger.info("下载完成")
        except Exception as e:
            logger.info(f"下载失败: {e}")
    elif re_download:
        logger.info("正在重新下载最新cards.json文件")
        try:
            download_json(json_path)
            logger.info("下载完成")
        except Exception as e:
            logger.info(f"下载失败: {e}")
    else:
        logger.info("cards.json已存在")

    with open(json_path, "r", encoding="utf8") as f:
        json_string = f.read()
        json_list = json.loads(json_string)
        json_dict = {}
        for item in json_list:
            json_dict[item["id"]] = item

    last_modified_time = datetime.fromtimestamp(os.path.getmtime(json_path)).strftime('%Y-%m-%d %H:%M:%S')
    return json_dict, last_modified_time

JSON_DICT, JSON_LAST_MODIFIED_TIME = read_json()

def query_json_dict(key):
    json_dict = JSON_DICT

    if key == "":
        return "Unknown"

    if key in json_dict:
        return json_dict[key]["name"]
    else:
        logger.info(f"未找到卡牌{key}，尝试重新下载cards.json文件")
        json_dict = read_json(True)
        if key not in json_dict:
            logger.error("出现未识别卡牌，程序无法继续")
            sys.exit(-1)
        return json_dict[key]["name"]

if __name__ == "__main__":
    with open("id-name.txt", "w", encoding="utf8") as f:
        for key, val in JSON_DICT.items():
            f.write(key + " " + val["name"] + "\n")

    query_json_dict("SW_085t")
