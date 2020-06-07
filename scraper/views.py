from django.shortcuts import render, redirect
from bs4 import BeautifulSoup
import requests
import json
from .models import Product
from .forms import SearchForm
from django.contrib.auth.decorators import login_required
import pandas as pd
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import numpy as np
from django.forms.utils import ErrorList

# Create your views here.
def home(request):
    with open('README.md', 'r', encoding='UTF-8')as f:
        content = f.read()
    return render(request, 'base.html', {'content': content})

def about(request):
    return render(request, 'users/about.html')

@login_required(login_url='login')
def extract(request):
    if request.method == 'POST':
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

        form = SearchForm(request.POST)
        if form.is_valid():
            product_id = str(form.cleaned_data['id'])
            url = url_prefix + "/" + product_id + url_postfix

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

            # Check if opinions for current product exist
            if not opinions_list:
                form.add_error('id', f'Nie znaliżiono opinij dla produktu z id: {product_id}.')
                return render(request, 'scraper/extract.html', {'form': form})

            #Dopóki nie znajdzie imie produktu (zrobione dla tego że link może otwórzyć nie od razu)
            product_name = None
            while product_name == None:
                page_response = requests.get("https://www.ceneo.pl/" + product_id)
                page_tree = BeautifulSoup(page_response.text, 'html.parser')
                product_name = page_tree.select("h1.product-name")
                print(product_name)

            # Analiza opinii
            opinions = pd.read_json(json.dumps(opinions_list))
            opinions = opinions.set_index("opinion_id")

            opinions["stars"] = opinions["stars"].map(lambda x: float(x.split("/")[0].replace(",", ".")))

            # histogram częstości występowania poszczególnych ocen
            stars = opinions["stars"].value_counts().sort_index().reindex(list(np.arange(0, 5.5, 0.5)), fill_value=0)
            fig, ax = plt.subplots()
            stars.plot.bar(color="lightskyblue")
            ax.set_title("Gwiazdki")
            ax.set_xlabel("liczba gwiazdek")
            ax.set_ylabel("liczba opinii")
            plt.savefig(f'media/opinion_analyze/{product_id}_bar.png')
            plt.close()

            # udział poszczególnych rekomendacji w ogólnej liczbie opinii
            recommendation = opinions["recommendation"].value_counts()
            fig, ax = plt.subplots()
            recommendation.plot.pie(label="", autopct="%1.1f%%", colors=['forestgreen', 'crimson'])
            ax.set_title("Rekomendacje")
            plt.savefig(f'media/opinion_analyze/{product_id}_pie.png')
            plt.close()

            # Jeśli ten id jest unikalny to dodaje go do bazy dannych
            try:
                Product.objects.get(product_id=product_id)

            except (Product.MultipleObjectsReturned, Product.DoesNotExist):
                Product.objects.create(
                    pros_amount=pros_amount,
                    cons_amount=cons_amount,
                    opinion_amount=opinion_amount,
                    product_id=product_id,
                    product_name=product_name[0].string,
                    mean=sum(mean) / len(mean),
                    opinions_list=opinions_list,
                    bar=f"opinion_analyze/{product_id}_bar.png",
                    pie=f"opinion_analyze/{product_id}_pie.png",
                )

            return redirect('product_info', product_id)
        return render(request, 'scraper/extract.html', {'form': SearchForm(request.POST)})
    return render(request, 'scraper/extract.html', {'form': SearchForm()})

# Create your views here.
@login_required(login_url='login')
def product_list(request):
    return render(request, 'product_list/product_list.html', {'products': Product.objects.all()})

@login_required(login_url='login')
def product_info(request, product_id):
    context = {
        'opinions': Product.objects.get(product_id=product_id).opinions_list,
        'pie': Product.objects.get(product_id=product_id).pie.url,
        'bar': Product.objects.get(product_id=product_id).bar.url,
    }
    return render(request, 'product_list/product_info.html', context)