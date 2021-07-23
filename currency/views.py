from django.shortcuts import render
from re import I
import requests
from bs4 import BeautifulSoup
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from currency.models import Currencies
from currency.serializer import CurrencySerializer


def homepage(request):
    url = 'https://www.tgju.org/currency'

    response = requests.get(url).text
    soup = BeautifulSoup(response, 'html.parser')
    search = soup.find_all(
        'tr')

    empty_list = []
    f = open('price.txt', 'a+')
    for item in search:
        try:
            empty_list.append(item.th.text)
        except:
            break
    empty_list.pop(-1)
    empty_list.pop(0)
    empty_list.pop(16)

    price_list = []
    price_list_un = []
    search_price = soup.find_all(
        'td', attrs={'class': 'nf'})

    for item in search_price:
        price_list_un.append(item.text)
    for price in price_list_un:
        if price_list_un.index(price) % 2 == 0:
            price_list.append(int(price.replace(',', '')) / 10)

    price_dict = dict(zip(empty_list, price_list))

    # for price in price_dict.items():
    #     name = list(price)
    # print(f'{name[0]} : {name[1]}')
    # print(price_dict)

    price_listed = list(price_dict.items())
    en_num = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    fa_num = ['۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹', '۰']
    dicted_prices = dict(zip(en_num, fa_num))

    print(price_listed)

    for item in price_listed:
        searched = Currencies.objects.filter(title__iexact=item[0]).exists()
        if not searched:
            Currencies.objects.create(title=item[0], price=item[1])
        elif searched:
            item_searched: Currencies = Currencies.objects.filter(title__iexact=item[0])
            item_price = Currencies.objects.filter(title__iexact=item[0]).first().price
            new_item_price = item[1]
            percentage = int(new_item_price) * 100 / int(item_price)
            if int(new_item_price) < int(item_price):
                item_searched.update(percentage=f'-{percentage}')

            elif int(new_item_price) > int(item_price):
                item_searched.update(percentage=f'+{percentage}')
            else:
                item_searched.update(percentage='0')
    prices: Currencies = Currencies.objects.all()
    context = {
        'prices': prices
    }
    return render(request, 'index.html', context)


class APISerializer(APIView):
    def get(self, request):
        query = Currencies.objects.all()
        serializer = CurrencySerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
