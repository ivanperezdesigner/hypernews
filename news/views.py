from django.conf import settings
from django.shortcuts import render, redirect
from django.views import View
import json
import random
from datetime import datetime

class BaseView(View):
    def get(self, request, *args, **kwargs):
        return redirect('/news/')

class NewsView(View):
    def get(self, request, news_id, *args, **kwargs):
        with open(settings.NEWS_JSON_PATH, 'r') as json_file:
            news_list = json.load(json_file)
        for i in news_list:
            if news_id == i['link']:
                new = i
        context = {
            'new': new
        }
        return render(request, 'news/new.html', context)

class MainView(View):
    def get(self, request, *args, **kwargs):
        with open(settings.NEWS_JSON_PATH, 'r') as json_file:
            news_list = json.load(json_file)
        def myFunc(e):
            return e['created']
        news_list.sort(reverse=True, key=myFunc)
        context = {
                'news_list': news_list,
        }
        # Query search
        query = str(request.GET.get('q'))
        for i in news_list:
            if query in i['title']:
                context = {
                    'news_list': [i]
                }
        return render(request, 'news/news.html', context)

class CreateView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'news/create.html')

    def post(self, request, *args, **kwargs):
        def random_link():
            link_list = []
            with open(settings.NEWS_JSON_PATH, 'r') as json_file:
                news_list = json.load(json_file)
            for i in news_list:
                link_list.append(i['link'])
            n = random.getrandbits(32)
            if n in link_list:
                n = random.getrandbits(32)
            else:
                return n

        new_dict = {
            'created': str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            'text': request.POST.get('text'),
            'title': request.POST.get('title'),
            'link': random_link()
        }
        with open(settings.NEWS_JSON_PATH) as f:
            data = json.load(f)
        data.append(new_dict)
        with open(settings.NEWS_JSON_PATH, 'w') as f:
            json.dump(data, f)
        return redirect('/news/')
