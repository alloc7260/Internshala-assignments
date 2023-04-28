import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

def FindAlternateGroups(store_domain):
    products = []
    page_number = 1
    while True:
        url = f"{store_domain}/collections/all/products.json?page={page_number}"
        response = requests.get(url)
        if response.status_code != 200:
            break
        data = json.loads(response.text)
        if not data:
            break
        products += data['products']
        page_number += 1

    df = pd.json_normalize(products, record_path=['variants'], meta=['id', 'handle', 'title', 'vendor', 'product_type'], record_prefix='option_')
    df['unique_attrs'] = df.apply(lambda row: f"{row['vendor']}_{row['title']}_{row.get('option_Size')}_{row.get('option_Color')}", axis=1)

    alternate_groups = []
    for unique_attrs, group in df.groupby('unique_attrs'):
        product_links = group['handle'].apply(lambda handle: f"{store_domain}/products/{handle}").tolist()
        alternate_group = {"product alternates": product_links}
        alternate_groups.append(alternate_group)

    return json.dumps(alternate_groups)

store_domain = "https://www.boysnextdoor-apparel.co"
# store_domain = "https://www.woolsboutiqueuomo.com"
# store_domain = "https://sartale2022.myshopify.com"
# store_domain = "https://berkehome.pl"
# store_domain = "https://glamaroustitijewels.com"
# store_domain = "https://lampsdepot.com"
# store_domain = "https://kitchenoasis.com"
print(FindAlternateGroups(store_domain))