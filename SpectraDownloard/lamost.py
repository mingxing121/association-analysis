import pandas as pd

# !/usr/bin/python
# -*- coding: UTF-8 -*-
# packages needed: urllib.request, urllib.parse, requests, pyfits, numpy, scipy.signal
import os
import urllib.request
import urllib.parse
import requests
import astropy.io.fits
import numpy
import scipy.signal
import matplotlib.pyplot as plt
import json
from retrying import retry

class lamost:
    def __init__(self, isdev=False, dataset=5):
        self.__isdev = isdev
        self.dataset = dataset
        self.email = None
        self.token = None
        self.version = None
        self.__isdev = False
        self.retry_times = 3
        self.timeout = 10

    def __getDataset(self):
        prefix = 'dr5'
        if self.dataset is not None:
            prefix = 'dr%d' % self.dataset
        if self.__isdev:
            return 'l' + prefix
        else:
            return prefix

    def __getVersion(self):
        if self.version is not None:
            return '/v%.1f' % self.version
            # return '/v%d' % self.version
        return ''

    __config = None
    __config_file_path = os.path.expanduser('~') + '/pylamost.ini'

    def __getConfig(self, reload=False):
        if not os.path.exists(self.__config_file_path): return None

        if not reload and None != self.__config: return self.__config

        with open(self.__config_file_path) as fh:
            self.__config = {}
            for line in fh:
                if line.startswith('#'): continue
                k, v = line.split("=")
                self.__config[k.strip()] = v.strip()
        return self.__config

    def __detectToken(self):
        if self.token is not None: return True
        cf = self.__getConfig()
        if cf is None or 'token' not in cf.keys():
            print('please set your token')
            return False
        self.token = cf['token']
        return True

    # 设置重试次数和超时时间
    retry_times = 3
    timeout = 30

    # 重试装饰器
    @retry(stop_max_attempt_number=retry_times, wait_fixed=timeout)
    def get_url_1(self,url,headers):
        request = urllib.request.Request(url=url, headers=headers)
        response = urllib.request.urlopen(request,timeout=self.timeout)
        return response

    def download(self, url, savedir='./'):

        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57'}
        # 下面三行不动
        # request = urllib.request.Request(url=url,headers=headers,method='POST')
        # response = urllib.request.urlopen(request,timeout=10)
        # data = response.read()

        response = self.get_url_1(url, headers)
        data = response.read()
        savefile = savedir + '/' + response.getheader("Content-disposition").split('=')[1]
        with open(savefile, 'wb') as fh:
            fh.write(data)
        return savefile

    # def getUrl(self, url, params=None):
    #     if params is None:
    #         response = urllib.request.urlopen(url)
    #     else:
    #         response = urllib.request.urlopen(url, urllib.parse.urlencode(params).encode('utf-8'))
    #     chrset = response.headers.get_content_charset()
    #     if chrset is None: chrset = 'utf-8'
    #     data = response.read().decode(chrset)
    #     return data

    def downloadCatalog(self, catname, savedir='./'):
        caturl = 'http://{0}.lamost.org{1}/catdl?name={2}&token={3}'.format(self.__getDataset(), self.__getVersion(),
                                                                            catname, self.token)
        return self.download(url, savedir)

    def downloadFits(self, obsid, savedir='./'):
        if not self.__detectToken(): return
        fitsurl = 'http://www.lamost.org:80/{0}/{1}/spectrum/fits/{2}?token={3}'.format(self.__getDataset(),
                                                                                self.__getVersion(), obsid,self.token)
        return self.download(fitsurl, savedir)

    def downloadPng(self, obsid, savedir='./'):
        if not self.__detectToken(): return
        pngurl = 'http://{0}.lamost.org{1}/spectrum/png/{2}?token={3}'.format(self.__getDataset(), self.__getVersion(),
                                                                              obsid, self.token)
        return self.download(pngurl, savedir)

    def getFitsCsv(self, obsid):
        if not self.__detectToken(): return None
        url = 'http://{0}.lamost.org{1}/spectrum/fits2csv/{2}?token={3}'.format(self.__getDataset(),
                                                                                self.__getVersion(), obsid, self.token)
        return self.getUrl(url)

    def getInfo(self, obsid):
        if not self.__detectToken(): return None
        # url='http://{0}.lamost.org{1}/spectrum/info/{2}?token={3}'.format(self.__getDataset(), self.__getVersion(), obsid, self.token)
        # return self.getUrl(url, params)
        url = 'http://{0}.lamost.org{1}/spectrum/info/{2}'.format(self.__getDataset(), self.__getVersion(), obsid)
        info = self.getUrl(url, {'token': self.token})
        info = json.loads(info)
        res = {}
        for prop in info["response"]:
            res[prop["what"]] = prop["data"]
        return res

    # Cone Search Protocol
    def conesearch(self, ra, dec, radius):
        if not self.__detectToken(): return
        conesearchurl = 'http://{0}.lamost.org{1}/voservice/conesearch?ra={2}&dec={3}&sr={4}&token={5}'.format(
            self.__getDataset(), self.__getVersion(), ra, dec, radius, self.token)
        return self.getUrl(conesearchurl)

    # Simple Spectral Access Protocol
    def ssap(self, ra, dec, radius):
        if not self.__detectToken(): return
        ssapurl = 'http://{0}.lamost.org{1}/voservice/ssap?pos={2},{3}&size={4}&token={5}'.format(self.__getDataset(),
                                                                                                  self.__getVersion(),
                                                                                                  ra, dec, radius,
                                                                                                  self.token)
        return self.getUrl(ssapurl)

    def sql(self, sql):
        if not self.__detectToken(): return
        sqlurl = 'http://{0}.lamost.org{1}/sql/q?&token={2}'.format(self.__getDataset(), self.__getVersion(),
                                                                    self.token)
        return self.getUrl(sqlurl, {'output.fmt': 'csv', 'sql': sql})

    def query(self, params):
        if not self.__detectToken(): return
        qurl = 'http://{0}.lamost.org{1}/q?token={2}'.format(self.__getDataset(), self.__getVersion(), self.token)
        return self.getUrl(qurl, params)

    def query2(self, params, files):
        if not self.__detectToken(): return
        qurl = 'http://{0}.lamost.org{1}/q?token={2}'.format(self.__getDataset(), self.__getVersion(), self.token)
        r = requests.post(qurl, data=params, files=files)
        return str(r.text)






