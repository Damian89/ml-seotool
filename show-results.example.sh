SAVEDMODEL_QUERY="begriff"
QUERY="keyword zum gegenprüfen"

python3 tool.py top-topics "$SAVEDMODEL_QUERY"

python3 tool.py best-doc "$SAVEDMODEL_QUERY" "$QUERY"

python3 tool.py distances "$SAVEDMODEL_QUERY"
