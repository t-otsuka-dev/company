# --*-- coding: utf-8  --*--

import json
import urllib
import ssl
from bs4 import BeautifulSoup
from django.http import HttpResponse
from rest_framework.response import Response

ssl._create_default_https_context = ssl._create_unverified_context

class SearchCompany:
    def get_company(self, keyword):

        '''
        国税庁のAPIを利用
        APIDocs:http://www.houjin-bangou.nta.go.jp/documents/k-web-api-kinou-ver2.pdf
        APPID:Kseggs6g3MHBs

        Param
        :name(required),商号又は名称
        '''

        url = 'https://api.houjin-bangou.nta.go.jp/2/name?'
        appid = 'Kseggs6g3MHBs'
        contents = url + 'id=' + appid + '&name=' + urllib.parse.quote(keyword) + '&type=12'
        result = urllib.request.urlopen(contents)
        soup = BeautifulSoup(result, "lxml")
        items = soup.findAll("corporation")

        url_list = {}
        i = 0
        for item in items:

            #法人種別判定
            if item.find("kind") == None:
                kind = '不明'
            elif str(item.find("kind")) == "01":
                kind = '国の機関'
            elif str(item.find("kind")) == "02":
                kind = '地方公共団体'
            elif str(item.find("kind")) == "03":
                kind = '設立登記法人'
            else:
                kind = 'その他'

            #郵便番号判定
            if item.find("postcode") == None:
                postCode = ''
            else:
                postCode = item.find("postcode").text

            #都道府県判定
            if item.find("prefecturename") == None:
                prefectureName = ''
            else:
                prefectureName = item.find("prefecturename").text

            #市区町村判定
            if item.find("cityname") == None:
                cityName = ''
            else:
                cityName = item.find("cityname").text

            #詳細住所判定
            if item.find("streetnumber") == None:
                streetNumber = ''
            else:
                streetNumber = item.find("streetnumber").text


            url_list[str(i)] = { "name":item.find("name").text,
                                 "postCode": postCode,
                                 "prefectureName":prefectureName,
                                 "cityName": cityName,
                                 "streetNumber": streetNumber
                                 }
            i = i + 1

        return url_list