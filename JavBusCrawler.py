#-*- coding:utf-8 -*-
from __future__ import unicode_literals
import json
import os , re
import codecs
import requests
from pip._vendor.distlib.compat import raw_input
import random
import time
from urllib.parse import urlparse
from urllib.parse import unquote,quote
from subprocess import (PIPE, Popen) 
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.chrome.options import Options 
import json 
import time 
import base64 
import argparse 


class Aria2c:
    '''
    Example :
      client = Aria2c('localhost', '6800')
      # print server version
      print(client.getVer())
      # add a task to server
      client.addUri('http://example.com/file.iso')
      # provide addtional options
      option = {"out": "new_file_name.iso"}
      client.addUri('http://example.com/file.iso', option)
    '''
    IDPREFIX = "pyaria2c"
    ADD_URI = 'aria2.addUri'
    GET_VER = 'aria2.getVersion'

    def __init__(self, host, port, token=None):
        self.host = host
        self.port = port
        self.token = token
        self.serverUrl = "http://{host}:{port}/jsonrpc".format(**locals())

    def _genPayload(self, method, uris=None, options=None, cid=None):
        cid = IDPREFIX + cid if cid else Aria2c.IDPREFIX
        p = {
            'jsonrpc': '2.0',
            'id': cid,
            'method': method,
            'params': []
        }
        if self.token is not None:
            p['params'] = ["token:" + self.token]
        else:
            p['params'] = ["token:" + '']
        if uris:
            p['params'].append(uris)
        if options:
            p['params'].append(options)
        return p

    @staticmethod
    def _defaultErrorHandler(code, message):
        print("ERROR: {}, {}".format(code, message))
        return None

    def _post(self, action, params, onSuc, onFail=None):
        if onFail is None:
            onFail = Aria2c._defaultErrorHandler
        payloads = self._genPayload(action, *params)
        resp = requests.post(self.serverUrl, data=json.dumps(payloads))
        result = resp.json()
        if "error" in result:
            return onFail(result["error"]["code"], result["error"]["message"])
        else:
            return onSuc(resp)

    def addUri(self, uri, options=None):
        def success(response):
            return response.text

        return self._post(Aria2c.ADD_URI, [[uri, ], options], success)

    def getVer(self):
        def success(response):
            return response.json()['result']['version']

        return self._post(Aria2c.GET_VER, [], success)  

if __name__ == "__main__": 
        parser = argparse.ArgumentParser() 
        parser.add_argument('--name', help='JAV Name',required=True) 
        args = parser.parse_args() 
        options = Options() 
        link = []
        FileList = []
        client = Aria2c()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox") 
        driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', chrome_options=options)
        try:
            driver.get("https://www.javbus.com/search/{}".format(args.name))
            elem = driver.find_elements_by_css_selector("div ul.pagination li a")
            if not elem:
                page = 1
            else:
                page = elem[-2].text
            for p in range(1, int(page)+1):
                driver.get("https://www.javbus.com/search/{}/{}".format(args.name, p))
                for elem in driver.find_elements_by_css_selector("div.masonry div.masonry-brick a.movie-box"):
                    link.append(elem.get_attribute("href"))
            for l in link:
                FileList.clear()
                driver.get(l)
                ele = driver.find_elements_by_css_selector("div.movie table[id=magnet-table] tr td a")
                if not ele:
                    continue
                else:
                    for _file in ele:
                        if "GB" in _file.text:
                            FileList.append([float(_file.text.replace(" ", "").replace("GB", "")), _file.get_attribute("href")])
                            #print(_file.text.replace(" ", "").replace("GB", ""))
                        elif "MB" in _file.text:
                            FileList.append([float(_file.text.replace(" ", "").replace("MB", "")), _file.get_attribute("href")])
                    client.addUri(sorted(FileList, key=lambda x: float(x[0]), reverse=True)[0][1])
                time.sleep(0.6)
            driver.close()


        finally:
            driver.quit()

