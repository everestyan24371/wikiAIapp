import requests

keyword = "Python (programming language)"  # 你可以替换为其他测试关键词
response = requests.get("https://en.wikipedia.org/w/api.php", {
    "action": "query",
    "format": "json",
    "titles": keyword,
    "prop": "extracts",
    "exintro": True,
    "explaintext": True
})

data = response.json()
pages = data.get('query', {}).get('pages', {})
extract = next(iter(pages.values())).get('extract', 'No content found.')

print("Extracted content:")
print(extract)
