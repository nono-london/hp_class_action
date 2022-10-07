import requests
base_url= "https://h30434.www3.hp.com/t5/forums/searchpage/tab/message?filter=location&q=broken%20hinge&advanced=true&location=category:Notebook&collapse_discussion=true&search_type=thread&search_page_size=50"
page_source = requests.get(url=base_url)
print(page_source.text)
print(page_source.json())