from django.shortcuts import render
import requests
from requests.compat import quote_plus
from bs4 import BeautifulSoup
from . import  models
BASE_CRAGELIST_URL='https://losangeles.craigslist.org/search/bbb?query{}'
# Create your views here.
def index(request):
   return render(request,'base.html')
def newsearch(request):
   search=request.POST.get('search')
   models.Search.objects.create(search=search)
   final_url=BASE_CRAGELIST_URL.format(quote_plus(search))
   response=requests.get(final_url)
   data=response.text
   soup=BeautifulSoup(data, features='html.parser')
   post_listing=soup.find_all('li',{'class':'result-row'})
   final_posting=[]
   for post in post_listing:
      post_title=post.find(class_='result-title').text
      post_url=post.find('a').get('href')
      if post.find(class_='result-price'):
         post_price=post.find(class_='result-price').text
      else:
         post_price='N/A'
      BASE_IMAGE_URL='https://images.craigslist.org/{}_300x300.jpg'
      if post.find(class_='result-image').get('data-ids'):
         post_image_id=post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
         post_image_url=BASE_IMAGE_URL.format(post_image_id)
         print(post_image_url)
      else:
        post_image_url='https://craigslist.org/images/peace.jpg'

      final_posting.append((post_title,post_url,post_price,post_image_url))
      
   stuff_for_frontend={
      'content':search,
      'final_posting':final_posting,
   }
   return render(request,'myapp/new-search.html',stuff_for_frontend)