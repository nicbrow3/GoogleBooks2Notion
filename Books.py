import requests 

database_id = "97ee0dad-43dd-472f-a305-f1a1d8d88df2"
#database_id = "b87d2fbe-79e9-4e6a-b8d0-1fd960bf4fec" #Home wiki ID

notion_token = "secret_uODspXB7EwM1Vw0mQVVCNwnlFT6W6BeCjZvETtF3uPi"
google_books_api = "AIzaSyDrE8DT9CoGMuDmlZvrLEbnTciyiFKY454"

global book_title
book_title = ""
page_id = ""
headers = {}


#---------------------------
def get_database_pages(db_id, token):
    url = f"https://api.notion.com/v1/databases/{db_id}/query"
    global headers
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        return response.json()['results']
    else:
        return []

def check_titles_and_update(token, db_id):
    global book_title
    global page_id
    pages = get_database_pages(db_id, token)
    for page in pages:
        title_property_name = "Name"  # Adjust based on your actual title property name
        if title_property_name in page['properties']:
            page_title = page['properties'][title_property_name]['title'][0]['plain_text']
            if page_title.endswith('!'):
                page_id = page['id']
                book_title = page_title[:-1]
                # Your logic to update the page, e.g., update_page_count(api_key, page_id)
                #print(f"Page titled '{book_title}' ends with semicolon. Updating page ID {page_id}.")

check_titles_and_update(notion_token, database_id)

print("book title: " + book_title)
url = "https://www.googleapis.com/books/v1/volumes?q=intitle:"+book_title+"&key="+google_books_api
response = requests.get(url)
book_data = response.json()
# Assuming the first item in the items list is the book we're interested in
book = book_data['items'][0]['volumeInfo']
title = book.get('title', 'No title available')
authors = book.get('authors', ['No authors available'])
publisher = book.get('publisher', 'No publisher available')
page_count = book.get('pageCount', 'Page count not available')
#print("pages: "+str(page_count))
genres = book.get('categories', ['No genre available'])
print("genres: "+str(genres))
description = book.get('description', 'No description available')
ISBN_10 = book.get('industryIdentifiers', 'No ISBN available')
print("ISBN_10: "+str(ISBN_10))

update_url = f"https://api.notion.com/v1/pages/{page_id}"

update_payload = {
    "properties": {
        "Total Pages": {
            "number": page_count #integer
        },
        "Authors": {  # Adjusting for multi-select property
            "multi_select": [{"name": author} for author in authors]  # Assuming authors is a list of strings
        },
        "Genre": {  # Adjusting for multi-select property
            "multi_select": [{"name": genre} for genre in genres]  # Assuming categories is a list of strings
        },
        "Name": {  # This assumes "Name" is the title property in your Notion database
            "title": [{"text": {"content": title}}]  # Assuming title is a string
        }
    }
}

update_response = requests.patch(update_url, headers=headers, json=update_payload)

if update_response.status_code == 200:
    print("Property updated successfully.")
else:
    print(f"Failed to update property. Status code: {update_response.status_code}")