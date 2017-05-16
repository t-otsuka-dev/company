from django.shortcuts import render
from .model import SearchCompany
import json
from django.http import HttpResponse
from rest_framework.response import Response



def company_get(request):

    if "name" in request.GET:
        # query_paramが指定されている場合の処理
        keyword = request.GET.get("name")
    else:
        # query_paramが指定されていない場合の処理
        return HttpResponse('<h1>Param Not Found</h1>')

    result = SearchCompany.get_company('self', keyword)
    res = json.dumps(result, ensure_ascii=False)
    return HttpResponse(res)