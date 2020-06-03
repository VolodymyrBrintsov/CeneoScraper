from django.shortcuts import render
from django.shortcuts import render
from . import models
from bs4 import BeautifulSoup
import requests
import json
from .models import Product
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login')
def extract(request):
    return render(request, 'scraper/extract.html')

@login_required(login_url='login')
def extract_result(request):
    # Funkcja która pobiera opinie(Potrzebna ponieważ to ekonomia kodu)
    def extract_feature(opinion, selector, attribute=None):
        try:
            if not attribute:
                return opinion.select(selector).pop().get_text().strip()
            else:
                return opinion.select(selector).pop()[attribute]
        except IndexError:
            return ""

    # ilość wad, zalet, opinij i średnia ocena dla dodania ich do bazy dannych
    pros_amount = 0
    cons_amount = 0
    opinion_amount = 0
    mean = []

    # lista składowych opinii wraz z selektorami i atrybutami
    selectors = {
        "author": ['span.user-post__author-name'],
        "recommendation": ['span.user-post__author-recomendation > em'],
        "stars": ['span.user-post__score-count'],
        "content": ['div.user-post__text'],
        "pros": ['div.review-feature__col:has(div.review-feature__title--positives)'],
        "cons": ['div.review-feature__col:has(div.review-feature__title--negatives)'],
        "useful": ['button.vote-yes', "data-total-vote"],
        "useless": ['button.vote-no', "data-total-vote"],
        "purchased": ['div.review-pz'],
        "purchase_date": ['span.user-post__published > time:nth-of-type(1)', "datetime"],
        "review_date": ['span.user-post__published > time:nth-of-type(2)', "datetime"]
    }

    # funkcja do usuwania znaków formatujących
    def remove_whitespaces(text):
        try:
            for char in ["\n", "\r"]:
                text = text.replace(char, ". ")
            return text
        except AttributeError:
            pass

    # adres URL strony z opiniami
    url_prefix = "https://www.ceneo.pl"
    url_postfix = "#tab=reviews"

    # Sprawdza czy jest podany produkt id je integer
    try:
        product_id = int(request.POST.get('product_id'))

    # Jeśli nie to zwraca użytkownika do strony "extract" z error messege że podane id jest niepoprawne
    except:
        return render(request, 'scraper/extract.html', {"error_msg": "Nie prawidlowo podane ID!"})
    url = url_prefix + "/" + str(product_id) + url_postfix

    # pusta lista na opinie
    opinions_list = []
    while url is not None:
        # pobranie kodu HTML strony z adresu URL
        page_response = requests.get(url)
        page_tree = BeautifulSoup(page_response.text, 'html.parser')
        # wybranie z kodu strony fragmentów odpowiadających poszczególnym opiniom
        opinions = page_tree.select("div.js_product-review")

        # ekstrakcja składowyh dla pojedynczej opinii z listy
        for opinion in opinions:
            features = {key: extract_feature(opinion, *args)
                        for key, args in selectors.items()}
            features["opinion_id"] = int(opinion["data-entry-id"])
            features["purchased"] = True if features["purchased"] == "Opinia potwierdzona zakupem" else False
            features["useful"] = int(features["useful"])
            features["useless"] = int(features["useless"])
            features["content"] = remove_whitespaces(features["content"])
            print(features['content'])
            features["pros"] = remove_whitespaces(features["pros"])
            features["cons"] = remove_whitespaces(features["cons"])

            opinions_list.append(features)
            opinion_amount += 1

            if features['cons'] != "":
                cons_amount += 1

            if features['pros'] != "":
                pros_amount += 1

            mean.append(int(features['stars'][0]))

        try:
            url = url_prefix + \
                  page_tree.select(
                      f'a.pagination__next[href*="{product_id}/op"]')[0]["href"]

        except IndexError:
            url = None
    # Sprawdza czy oponion list nie jest pust
    # Jeśli jest to zwraca użytkownika do strony "extract/" z error message 'Nie znaliziono podanego Id'
    if len(opinions_list) == 0:
        return render(request, 'scraper/extract.html',
                      {'error_msg': f"Produkt z takim id:{product_id} nie został znalieżionym"})

    # Jeśli ten id jest unikalny to dodaje go do bazy dannych
    try:
        Product.objects.get(product_id=product_id)

    except (Product.MultipleObjectsReturned, Product.DoesNotExist):
        Product.objects.create(
            pros_amount=pros_amount,
            cons_amount=cons_amount,
            opinion_amount=opinion_amount,
            product_id=product_id,
            mean=sum(mean) / len(mean),
            opinions_list=opinions_list
        )

    context = {
        'comments_amount': len(opinions_list),
        'opinions': Product.objects.get(product_id=product_id).opinions_list
    }

    return render(request, 'scraper/extract_result.html', context)

# Wyświtla wśystkie produkty znajdojących w bazie dannych
