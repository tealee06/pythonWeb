import pandas as pd
import chardet
import random

file_path = 'C:/Users/sunbi/OneDrive/바탕 화면/books_data_with_sales_points.csv'
with open(file_path, 'rb') as f:
    result = chardet.detect(f.read())
file_encoding = result['encoding']
books_data = pd.read_csv(file_path, encoding=file_encoding)
books_data = books_data[['title', 'field', 'sales_point']]
books_data['sales_point'] = pd.to_numeric(books_data['sales_point'], errors='coerce')
books_data.dropna(inplace=True)
def recommend_books(field, num_recommendations=5):
    # 입력받은 분야에 해당하는 책 필터링
    field_books = books_data[books_data['field'].str.contains(field, case=False, na=False)]
    if len(field_books) <= num_recommendations:
        return field_books['title'].tolist()
    recommended_books = field_books.sample(num_recommendations)
    return recommended_books['title'].tolist()
def recommend_books_by_field():
    unique_fields = books_data['field'].unique()
    print("다음 중에서 추천받고 싶은 분야를 입력하세요:")
    for field in unique_fields:
        print(field)
    field = input("\n추천받고 싶은 분야를 입력하세요: ").strip()
    recommended_books = recommend_books(field, num_recommendations=5)
    if isinstance(recommended_books, list) and recommended_books:
        print("\n추천 도서 목록:")
        for i, book in enumerate(recommended_books, 1):
            print(f"{i}. {book}")
    else:
        print("해당 분야에 맞는 책을 찾을 수 없습니다.")
recommend_books_by_field()

