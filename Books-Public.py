# Python script for using the Google Books API and the Notion API to update book information in a Notion database.

import requests
import datetime

database_id = "<your Notion database id>"
notion_token = "<your secret notion token>"
latest_notion_version = "2022-06-28"  # Notion API version

google_books_api = "<your google books api key>"

line_end_char = ":"

global book_title
book_title = ""
page_id = ""
headers = {}

# Makes a POST request to the Notion API to retrieve database pages based on the provided db_id and token"


def get_database_pages(db_id, token):
    url = f"https://api.notion.com/v1/databases/{db_id}/query"
    global headers
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Notion-Version": latest_notion_version
    }
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        return response.json()['results']
    else:
        return []


# Retrieves pages from a Notion database, extracts the title of each page, searches Google Books for matching titles and updates the corresponding page in a Notion database with the retrieved information, such as book title, authors, publisher, summary, ISBNs, and more. It uses the retrieved data to construct a request to update the properties of a Notion page using the Notion API.
def check_titles_and_update(token, db_id):
    global book_title
    global page_id
    pages = get_database_pages(db_id, token)
    for page in pages:
        title_property_name = "Title"  # Adjust based on your actual title property name
        if title_property_name in page['properties']:
            page_title = page['properties'][title_property_name]['title'][0]['plain_text']
            if page_title.endswith(line_end_char):
                page_id = page['id']
                book_title = page_title[:-1]
                url = "https://www.googleapis.com/books/v1/volumes?q=intitle:" + \
                    book_title+"&key="+google_books_api
                response = requests.get(url)
                book_data = response.json()
                # Assuming the first item in the items list is the book we're interested in
                book = book_data['items'][0]['volumeInfo']
                title = book.get('title', 'No title available')
                authors = book.get('authors', ['No authors available'])
                publisher = book.get('publisher', 'No publisher available')
                published_date = book.get(
                    'publishedDate', 'No published date available')
                page_count = book.get('pageCount', 'Page count not available')
                try:
                    cover_image_url = book_data['items'][0]['volumeInfo']['imageLinks']['thumbnail']
                except KeyError:
                    cover_image_url = ''
                genres = []
                for category in book.get('categories', []):
                    genres.append(category)

                summary = book.get('description', 'No description available')
                # Truncate summary to 2000 characters (notion limit for rich_text)
                if summary and len(summary) > 2000:
                    summary = summary[:1997] + "..."

                ISBN_10 = next((identifier['identifier'] for identifier in book.get(
                    'industryIdentifiers', []) if identifier['type'] == 'ISBN_10'), 'No ISBN available')
                ISBN_13 = next((identifier['identifier'] for identifier in book.get(
                    'industryIdentifiers', []) if identifier['type'] == 'ISBN_13'), 'No ISBN available')

                # cover_image_url = get_audiobook_cover(title, google_books_api)

                update_url = f"https://api.notion.com/v1/pages/{page_id}"

                update_payload = {  # properties that we're editing in the target page

                    "properties": {
                        "Total Pages": {
                            "number": page_count  # integer
                        },
                        "Authors": {  # Adjusting for multi-select property
                            "multi_select": [{"name": author} for author in authors]
                        },
                        "Category": {
                            "multi_select": [{"name": genre} for genre in genres]},
                        "Title": {
                            "title": [{"text": {"content": title}}]
                        },
                        "Publisher": {
                            "rich_text": [{"text": {"content": publisher}}]
                        },
                        "Summary": {
                            "rich_text": [{"text": {"content": summary}}]
                        },
                        "ISBN_10": {
                            "rich_text": [{"text": {"content": ISBN_10}}]
                        },
                        "ISBN_13": {
                            "rich_text": [{"text": {"content": ISBN_13}}]
                        },
                        "Published": {
                            "date": {
                                "start": published_date
                            }
                        },
                        "Dates Read": {  # Assuming "Read Property" is the name of the date range property
                            "date": {
                                "start": str(datetime.date.today()),
                                "end": str(datetime.date.today() + datetime.timedelta(days=7))
                            }
                        },
                        "Image": {
                            "type": "files",
                            "files": [
                                {
                                    "name": "Cover Image",  # Optional name for the file
                                    "type": "external",
                                    "external": {
                                        "url": cover_image_url
                                    }
                                }
                            ]
                        }
                    },
                    "icon": {
                        "type": "external",
                        "external": {
                            "url": cover_image_url
                        }
                    },
                    "cover": {
                        "type": "external",
                        "external": {
                            "url": cover_image_url
                        }
                    }
                }

                # print(update_payload)
                update_response = requests.patch(
                    update_url, headers=headers, json=update_payload)

                if update_response.status_code == 200:
                    print("Property updated successfully.")
                else:
                    print(f"Failed to update property. Status code: {
                          update_response.status_code}")
                    print(update_response.json())


check_titles_and_update(notion_token, database_id)
