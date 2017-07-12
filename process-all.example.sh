SAVEDMODEL_QUERY="suchbegriff"

# 1. extract top 100 from google
python3 tool.py scrape "$SAVEDMODEL_QUERY"

# 2. extract content 
python3 tool.py extract "$SAVEDMODEL_QUERY" 100 500

# 3. clean, content, remove stopwords, ...
python3 tool.py prepare "$SAVEDMODEL_QUERY" 3 2 100

# 4. train models and save
python3 tool.py train "$SAVEDMODEL_QUERY" 165

# INFO: Do not use this chain over and over, use the appropriate command from the list above!
# For most cases you dont need to scrape google over and over again for the same query ;)