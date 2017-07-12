SAVEDMODEL_QUERY="begriff"

QUERY="keyword zum gegenprüfen, kann auch das gleiche wie savedmodel_query sein"

# 1. Extract top topics
python3 tool.py top-topics "$SAVEDMODEL_QUERY"

# 2. Get the best document in trained models for query
python3 tool.py best-doc "$SAVEDMODEL_QUERY" "$QUERY"

# 3. Get the distances between every document
python3 tool.py distances "$SAVEDMODEL_QUERY"
