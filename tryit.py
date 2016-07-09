#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
import sys
import re
import argparse

from wordcloud import WordCloud
import jieba
import requests
from lxml import html

def read_stopwords(file):
    stopwords = set()
    with open(file, 'rb') as f:
        for line in f.readlines():
            if not line.strip():
                continue
            stopwords.add(line.strip().decode('utf-8'))
    return stopwords
stopwords = read_stopwords(path.join(path.dirname(__file__), 'stopwords.txt'))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', metavar='URL', required=True, help='input the url')
    args = parser.parse_args()

    output_file = path.join(path.dirname(__file__), 'wordcloud.png')

    url = args.url

    response = requests.get(url, timeout=15)
    response.encoding = response.apparent_encoding

    origin_text = response.text
    origin_text = re.sub(ur'<script.*?>.*?</script>', '', origin_text, flags=re.I|re.M|re.DOTALL)
    origin_text = re.sub(ur'<style.*?>.*?</style>', '', origin_text, flags=re.I|re.M|re.DOTALL)

    doc = html.fromstring(origin_text)
    text = doc.xpath('//body//text()')
    text = [i.strip() for i in text if i.strip()]
    text = u' '.join(text)

    seg = jieba.cut(text)
    seg = [i.strip() for i in seg if i.strip() and not i.strip().isdigit() and i.strip() not in stopwords]
    seg = u' '.join(seg)

    wordcloud = WordCloud(font_path='simhei.ttf', background_color='black', margin=5, width=1800, height=800)
    wordcloud = wordcloud.generate(seg)
    image = wordcloud.to_image()

    with open(output_file, 'wb') as f:
        image.save(f, format='png')

if __name__ == '__main__':
    main()
