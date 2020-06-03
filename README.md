# CeneoScraper
Aplikacja pozwala na pobieranie, oraz analizę opinii o produktach ze strony Ceneo.pl, co uchroni Cię przed nietrafionym zakupem
# Jak korzystać?
- Trzeba kliknąć na "Ekstrakcja opinii"
- Wpisać kod produktu, który jest ciekawy dla Państwa
- Każdy nowy kod będżie zapisany do bazy dannych postgreSQL oraz opinii o tym produkcie. Znależione produkty będą wyświetlane w "Lista produktow"
- Po poberaniu dannych będżie możliwe popatrzyć na statystyczne dane oraz pobrać plik z dannymi
- W zakładce "O Projekcie" można znależć link do github'a
## Dla każdej opinii pobierane są:
- opinia: div.js_product-review
- identyfikator: div.js_product-review["data-entry-id"]
- autor: div.reviewer-name-line
- rekomendacja: div.product-review-summary > em
- liczba gwiazdek: span.review-score-count
- czy potwierdzona zakupem: div.product-review-pz
- data wystawienia: span.review-time > time["datetime"] - pierwsze wyystąpienie
- data zakupu: span.review-time > time["datetime"] - drugie wyystąpienie
- przydatna: button.vote-yes["data-total-vote"]
- nieprzydatna: button.vote-no["data-total-vote"]
- treść: p.product-review-body
- wady: div.cons-cell > ul
- zalety: div.pros-cell > ul
## Zastosowane technologie:
Aplikacja została napisana z wykorzystaniem: Python, Django, BeautifullSoup, Bootstrap, PostreSQL