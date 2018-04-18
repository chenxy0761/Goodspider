# -*- coding:utf-8 -*-
from scrapy import cmdline

cmdline.execute("scrapy crawl jd --logfile log/Jd.log".split())
# cmdline.execute("scrapy crawl test".split())