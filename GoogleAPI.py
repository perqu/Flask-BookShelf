from urllib.request import urlopen
import json


def GetBookData(bookName):
    bookName = bookName.replace(" ", "%20")
    url = f"https://www.googleapis.com/books/v1/volumes?q={bookName}"

    # store the response of URL
    response = urlopen(url)

    # storing the JSON response
    data_json = json.loads(response.read())

    selected_data = []

    for i in range(5):

        temp = {}

        # counter
        temp["id"] = i + 1
        # title
        try:
            temp["title"] = data_json["items"][i]["volumeInfo"]["title"]
        except:
            temp["title"] = "Not provided"
        # authors
        try:
            temp["authors"] = data_json["items"][i]["volumeInfo"]["authors"]
        except:
            temp["authors"] = "Not provided"
        # published_date
        try:
            temp["published_date"] = data_json["items"][i]["volumeInfo"][
                "publishedDate"
            ]
        except:
            temp["published_date"] = "Not provided"
        # ISBN10
        try:
            industry_identifiers = data_json["items"][i]["volumeInfo"]["industryIdentifiers"]
            for el in industry_identifiers:
                if el['type']=='ISBN_10':
                    temp["ISBN10"] = el['identifier']
            if 'ISBN10' not in temp.keys():
                temp["ISBN10"] = "Not provided"
        except:
            temp["ISBN10"] = "Not provided"
        # ISBN13
        try:
            industry_identifiers = data_json["items"][i]["volumeInfo"]["industryIdentifiers"]
            for el in industry_identifiers:
                if el['type']=='ISBN_13':
                    temp["ISBN13"] = el['identifier']
            if 'ISBN13' not in temp.keys():
                temp["ISBN13"] = "Not provided"
        except:
            temp["ISBN13"] = "Not provided"
        # page_count
        try:
            temp["page_count"] = data_json["items"][i]["volumeInfo"]["pageCount"]
        except:
            temp["page_count"] = 0
        # preview_link
        try:
            temp["preview_link"] = data_json["items"][i]["volumeInfo"]["previewLink"]
        except:
            temp["preview_link"] = "Not provided"
        # language
        try:
            temp["language"] = data_json["items"][i]["volumeInfo"]["language"]
        except:
            temp["language"] = "Not provided"

        selected_data.append(temp)

    return selected_data

GetBookData("harry")