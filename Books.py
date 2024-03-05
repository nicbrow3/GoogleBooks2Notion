import requests

api_key = "AIzaSyDrE8DT9CoGMuDmlZvrLEbnTciyiFKY454"
ISBN_10 = "0316387347"
book_title = "Before they are hanged"
url = "https://www.googleapis.com/books/v1/volumes?q=intitle:"+book_title+"&key="+api_key


response = requests.get(url)
data = response.json()

# Assuming the first item in the items list is the book we're interested in
book = data['items'][0]['volumeInfo']

title = book.get('title', 'No title available')
authors = book.get('authors', ['No authors available'])
publisher = book.get('publisher', 'No publisher available')
page_count = book.get('pageCount', 'Page count not available') # If the page count is not available, the value will be 'Page count not available'
categories = book.get('categories', ['No categories available'])

print(f"Title: {title}")
print(f"Authors: {', '.join(authors)}")
print(f"Publisher: {publisher}")
print(f"Page Count: {page_count}")
print(f"Categories: {', '.join(categories)}")
