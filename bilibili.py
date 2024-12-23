#!/usr/bin/env python3 | coding=utf-8

# code : Aldi Bachtiar Rifai
# type : Tool downloader bstation | open source code team

import requests
import re
import os
from rich import print as print_json
import pyfiglet

# def get_video_id
def get_video_id(url):
    """
    Mengambil video ID dari URL video.
    """
    match = re.search(r'/video/(\d+)', url)
    if match:
        return match.group(1)
    return None

# def get_title
def get_title(url):
    """
    Mengambil judul video dari halaman HTML.
    """
    response = requests.get(url)
    title_match = re.search("<title>(.*?)</title>", response.text)
    if title_match:
        return title_match.group(1)
    return "Unknown Title"

# def get_video_urls
def get_video_urls(video_id, title):
    """
    Mengambil URL video dari API.
    """
    url = "https://api.bilibili.tv/intl/gateway/web/playurl"
    params = {
        "s_locale": "en_US",
        "platform": "html5_a",
        "aid": video_id,
        "qn": "64",
        "type": "0",
        "device": "wap",
        "tf": "0",
        "spm_id": "bstar-web.ugc-video-detail.0.0",
        "from_spm_id": ""
    }
    headers = {
        "authority": "api.bilibili.tv",
        "accept": "application/json, text/plain, */*",
        "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
        "cookie": "buvid3=5d7ab82a-30aa-4f72-91be-fa0ef656a34864680infoc; bstar-web-lang=id; _ga=GA1.1.1172665079.1733307593; _ga_X4BG3JXFB1=GS1.1.1733307593.1.1.1733307615.0.0.0",
        "origin": "https://www.bilibili.tv",
        "referer": f"https://www.bilibili.tv/en/video/{video_id}?s_locale=in_ID&from=COPY",
        "sec-ch-ua": '"Not-A.Brand";v="99", "Chromium";v="124"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"Android"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
    }

    response = requests.get(url, params=params, headers=headers)
    array_video = []
    if response.status_code == 200:
        for video in response.json()['data']['playurl']['video']:

            # Output
            array_video.append({
                "title": title.encode("latin1").decode("utf-8"),
                "url": video['video_resource']['url'],
                "url_backup": video['video_resource']['backup_url'][0],
                "quality": video['stream_info']['desc_words'],
                "mime_type": video['video_resource']['mime_type'],
            })
    return array_video

# Main
if __name__ == "__main__":
    os.system("clear")
    ascii_art = pyfiglet.figlet_format("BiLiDoWn")
    print (ascii_art)
    print ("-"*25)
    video_page_url = input(" - Input url : ")
    video_id = get_video_id(str(video_page_url))
    if video_id:
        video_title = get_title(video_page_url)
        try:
            video_urls = get_video_urls(video_id, video_title)
            print ("-"*25)
            print (f" - Title      : {video_urls[0]['title']}")
            print (f" - Quality    : {video_urls[0]['quality']}")
            print (f" - Url        : {video_urls[0]['url']}")
            print (f" - Url Backup : {video_urls[0]['url_backup']}") 
            print (f" - Results Type Json: ")
            print_json(video_urls)
            print ("-"*25)
        except Exception as error:print ("-"*25);print (f" - Error: {error}");print ("-"*25)
    else:
        print (" - Video ID tidak ditemukan.");print ("-"*25)
