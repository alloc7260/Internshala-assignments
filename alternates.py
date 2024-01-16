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







#######################################################################################################################################################################################################################
"""
Problem statement

Hey there,

Roll up your sleeves, as you have been qualified for the skill assessment stage. As part of this stage, we have created a task called "Find Product Alternates" to evaluate your AI skills.

For further information about the task, please click on the link provided below:
https://laser-comb-669.notion.site/Help-shoppers-find-product-variations-2eec9b82b7c14c9eb849f481db83a14e

You must complete the task within 48 hours and share the link of your code in the chat. 

We appreciate your time and effort in completing this task, and we are looking forward to seeing your code. If you have any questions or require assistance, please do not hesitate to contact us.

Best regards,
Shubham Vats
StarApps Studio
"""
