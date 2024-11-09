from flask import Flask, request, jsonify
from flask_cors import CORS  # 导入 CORS
from transformers import pipeline
import requests

app = Flask(__name__)
CORS(app)  # 启用 CORS

# 创建总结器
print("Initializing summarization pipeline...")
summarizer = pipeline("summarization")
print("Summarization pipeline initialized.")

@app.route('/summarize', methods=['GET'])
def summarize_wiki():
    keyword = request.args.get('keyword')
    if not keyword:
        return jsonify({"error": "Keyword is required"}), 400

    # 使用 MediaWiki API 抓取内容
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

    # 调用 NLP 模型生成摘要
    if extract != 'No content found.':
        print(f"Generating summary for keyword: {keyword}")
        summary = summarizer(extract, max_length=100, min_length=30, do_sample=False)
        return jsonify({"summary": summary[0]['summary_text']})
    else:
        print(f"No content found for keyword: {keyword}")
        return jsonify({"error": "No content found for the given keyword"}), 404

if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(debug=True)
