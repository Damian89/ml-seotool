SAVEDMODEL_QUERY="suchbegriff"

python3 tool.py scrape "$SAVEDMODEL_QUERY"

python3 tool.py extract "$SAVEDMODEL_QUERY" 100 500

python3 tool.py prepare "$SAVEDMODEL_QUERY" 3 2

python3 tool.py train "$SAVEDMODEL_QUERY" 165

