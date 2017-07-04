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

