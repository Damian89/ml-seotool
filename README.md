#Machine Learning/Statistik SEO Tool

Simples Tool, das einige ML/Statistik Algorithmen für die Analyse von Textdokumenten verwendet. Das ganze ist recht "modular" aufgebaut - von einem Python-Noob :P

## Funktionen

- Abrufen der Top 100 von Google.de zu einem Suchbegriff
- Extraktion des Inhalts der Top 100
- Generierung von Tokens, Dictionaries und Corpi mit Gensim/SKLearn
- Trainieren diverser Algorithmen sowie deren Persistenz
- Abrufen der Ergebnisse

## Algorithmen

- Latent Semantic Indexing via Gensim
    - Allgemein für Transformation der Corpi
- TFIDF + Latent Semantic Indexing via Gensim
    - Themen-Extraktion
    - Bestes Dokument zur Suche
- Latent Dirichlet Allocation via Gensim
    - Top Topic Extraction
    - Bestes Dokument zur Suche
- Hierarchical Dirichlet Process via Gensim
    - Top Topic Extraction
    - Bestes Dokument zur Suche
- TFIDF + Latent Dirichlet Allocation via Sklearn
    - Top Topic Extraction
- TFIDF + Non-negative matrix factorization
    - Top Topic Extraction
- Spotify Annoy
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

Auf die Schnell kann man die "process-all.sh" öffnen und das Suchwort ändern. Anschließed ausführen via sh. Dabei wird für die Suchquery die Top 100 von google.de (!) heruntergeladen, anschließend wird jedes Ergebnis gecrawled und dessen Content extrahiert.

<strong>Achtung:</strong> Das Tool erkennt recht simpel englische Texte und skipped solchen Content. Wenn anderes Vorgehen erwünscht ist, muss man die entsprechenden Dateien anpassen (extract.py). Gleiches gilt für die Extraktion der Top 100. Hier werden bestimmte Seiten übersprungen (youtube.com, .ru-Links, Foren, ...). Ist aber leicht anpassbar.

<strong>Alternativ von Hand:</strong>

python3 tool.py scrape "4k fernseher" <br />
python3 tool.py extract "4k fernseher" 100 500 <br />
python3 tool.py prepare "4k fernseher" 3 <br />
python3 tool.py train "4k fernseher" 165 <br />

Die Parameter (meist Zahlen) definieren, meist wie viele Ergebnisse verwendet werden sollen, wie groß der Corpus sein soll, wie groß ein Wort min. sein muss. Im Quellcode gibt es eig. direkt konkrete Antwort.

<em>Die "process-all.sh" ist vor allem dann einfacher, wenn man zuvor noch kein Crawl gemacht hat. Sind die Daten einmal da, sollte man für das Vorbereiten/Neu trainieren manuell anstoßen.</em>

## Ergebnisse anzeigen

Wichtig ist, dass process-all.sh zuvor ausgeführt wurde - damit die Modelle trainiert sind und es überhaupt Daten geben kann.
Auch hier kann man allesauf einmal mit "show-results.sh" anzeigen lassen. Zuvor den Suchbegriff analog der "process-all.py" anpassen.

<strong>Alternativ von Hand:</strong>

python3 tool.py top-topics "4k fernseher" <br />
python3 tool.py best-doc "4k fernseher"<br />
python3 tool.py distances "4k fernseher"<br />