from flask import Flask, request, render_template
import pandas as pd
import chardet
import plotly.express as px
import os

app = Flask(__name__)

# 데이터 로드
file_path = 'books_data_with_sales_points.csv'
with open(file_path, 'rb') as f:
    result = chardet.detect(f.read())
file_encoding = result['encoding']
books_data = pd.read_csv(file_path, encoding=file_encoding)
books_data = books_data[['title', 'field', 'sales_point']]
books_data['sales_point'] = pd.to_numeric(books_data['sales_point'], errors='coerce')
books_data.dropna(inplace=True)

@app.route('/')
def home():
    fields = books_data['field'].unique()
    return render_template('index.html', fields=fields)

@app.route('/recommend', methods=['POST'])
def recommend():
    field = request.form.get('field')
    field_books = books_data[books_data['field'].str.contains(field, case=False, na=False)]
    top_field_books = field_books.nlargest(10, 'sales_point')  # 판매 포인트 기준 상위 10권 선택
    fig = px.bar(top_field_books, x='title', y='sales_point', title=f'{field} 분야 도서 판매 포인트')
    fig.update_layout(height=900)  # 세로 길이를 늘림 (기본값의 약 3배)
    graph_html = fig.to_html(full_html=False)
    recommendations = top_field_books['title'].tolist()
    return render_template('index.html', recommendations=recommendations, fields=books_data['field'].unique(), selected_field=field, graph_html=graph_html)

if __name__ == '__main__':
    app.run(debug=True)
