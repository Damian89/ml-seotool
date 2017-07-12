# Machine Learning/Statistik SEO Tool

Simples Tool, das einige ML/Statistik Algorithmen für die Analyse von Textdokumenten verwendet. Das ganze ist recht "modular" aufgebaut - von einem Python-Noob :P

## Funktionen

- Abrufen der Top 100 von Google.de zu einem Suchbegriff
- Extraktion des Inhalts der Top 100
- Generierung von Tokens, Dictionaries und Corpi mit Gensim/SKLearn
- Trainieren diverser Algorithmen sowie deren Persistenz
- Abrufen der Ergebnisse

## Algorithmen

- Latent Semantic Indexing via <strong>Gensim</strong>
    - Allgemein für Transformation der Corpi
- TFIDF + Latent Semantic Indexing via <strong>Gensim</strong>
    - Themen-Extraktion
    - Bestes Dokument zur Suche
- Latent Dirichlet Allocation via <strong>Gensim</strong>
    - Top Topic Extraction
    - Bestes Dokument zur Suche
- Hierarchical Dirichlet Process via <strong>Gensim</strong>
    - Top Topic Extraction
    - Bestes Dokument zur Suche
- TFIDF + Latent Dirichlet Allocation via <strong>Sklearn</strong>
    - Top Topic Extraction
- TFIDF + Non-negative matrix factorization via <strong>Sklearn</strong>
    - Top Topic Extraction
- Approximate Nearest Neighbors via <strong>Spotify Annoy</strong>
    - Bestes Dokument zur Suche
    - Distanz zwischen Dokumenten

## Voraussetzungen

- Python 3.5
- Sklearn
- Numpy
- annoy
- gensim
- BeautifilSoup

Allgemein ist es empfehlenswert einfach auf die Fehlermeldungen zu achten und ggf. einfach via pip zu installieren: "pip install gensim" beispielsweise. Das Tool hat recht viele Abhängigkeiten!

## Verwendung

Auf die Schnell kann man die "process-all.sh" öffnen und das Suchwort ändern. Anschließed ausführen via sh. Dabei wird für die Suchquery die Top 100 von google.de (!) heruntergeladen, anschließend wird jedes Ergebnis gecrawled und dessen Content extrahiert. Alle Daten werden in das sluggified Verzeichnis innerhalb von "data/" gespeichert. Daher ist der erste Parameter der Befehle meist die Suche mit der die Daten abgerufen wurden!

<strong>Achtung:</strong> Das Tool erkennt recht simpel englische Texte und skipped solchen Content. Wenn anderes Vorgehen erwünscht ist, muss man die entsprechenden Dateien anpassen (extract.py). Gleiches gilt für die Extraktion der Top 100. Hier werden bestimmte Seiten übersprungen (youtube.com, .ru-Links, Foren, ...). Ist aber leicht anpassbar.

<strong>Alternativ von Hand:</strong>

<em>Scrapen:</em><br />
```
python3 tool.py scrape "4k fernseher"
```

<em>Extrahiere Content von min. 20 (der zuvor gescrapten Links), Minimale Anzahl von Wörtern muss 500 betragen:</em><br />
```
python3 tool.py extract "4k fernseher" 20 500
```

<em>Corpus vorbereiten - Mindestlänge der Wörter: 3 Zeichen, Mindestvorkommen der Wörter: 2x, nutze 100 Dokumente, wenn verfügbar:</em><br />
```
python3 tool.py prepare "4k fernseher" 3 2 100
```

<em>Trainiere Modelle für min. 45 Themen:</em><br />
```
python3 tool.py train "4k fernseher" 45
```

Die Parameter (meist Zahlen) definieren, meist wie viele Ergebnisse verwendet werden sollen, wie groß der Corpus sein soll, wie groß ein Wort min. sein muss. Im Quellcode gibt es eig. direkt konkrete Antwort.

<em>Die "process-all.sh" ist vor allem dann einfacher, wenn man zuvor noch kein Crawl gemacht hat. Sind die Daten einmal da, sollte man für das Vorbereiten/Neu trainieren manuell anstoßen.</em>

## Ergebnisse anzeigen

Wichtig ist, dass process-all.sh zuvor ausgeführt wurde - damit die Modelle trainiert sind und es überhaupt Daten geben kann.
Auch hier kann man allesauf einmal mit "show-results.sh" anzeigen lassen. Zuvor den Suchbegriff analog der "process-all.py" anpassen.

<strong>Alternativ von Hand:</strong>
<em>Extrahiert die Themenkomplexe:</em><br />
```
python3 tool.py top-topics "4k fernseher"
```

<em>Zeigt an, welche Dokuemten am besten auf ein Suchbegriff (hier "smart tv") passen:</em><br />
```
python3 tool.py best-doc "4k fernseher" "smart tv"
```

<em>Vergleicht die Distanz zw. allen Dokumenten:</em><br />
```
python3 tool.py distances "4k fernseher"
```


## Sonstiges

### Stoplisten

In data/statics findet man einige Stoplisten, die automatisch eingelesen und verwendet werden. Je nach Case lohnt sich da was rein/rauszunehmen. Sieht man dann meist während der Ergebnisse, dass Crap dabei ist. Dann einfach Datei anpassen und prepare.py + train.py, wie oben beschrieben, ausführen.

### Google Scraping

Zu schnelles Scrapen führt bei Google schnell zum Ausschluss. Ich schalge max. jede 2 Minuten vor.