QUERY="dolby vision1"

#python3 tool.py scrape "$QUERY"

#python3 tool.py extract "$QUERY" 100 500

python3 tool.py prepare "$QUERY" 1

python3 tool.py train "$QUERY" 165

