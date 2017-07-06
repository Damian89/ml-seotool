SAVEDMODEL_QUERY="begriff"

QUERY="keyword zum gegenprüfen, kann auch das gleiche wie savedmodel_query sein"

python3 tool.py top-topics "$SAVEDMODEL_QUERY"

python3 tool.py best-doc "$SAVEDMODEL_QUERY" "$QUERY"

python3 tool.py distances "$SAVEDMODEL_QUERY"
