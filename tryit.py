#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
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

stopwords = read_stopwords('stopwords.txt')

url = sys.argv[1]
ret = requests.get(url)
ret.encoding = ret.apparent_encoding
origin_text = ret.text
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
with open('wordcloud.png', 'wb') as f:
    image.save(f, format='png')


