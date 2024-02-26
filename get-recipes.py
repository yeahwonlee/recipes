import json
import requests
import threading
# from tqdm import tqdm
from bs4 import BeautifulSoup

def lambda_handler(event, context):
    # TODO implement
    url = 'https://www.foodnetwork.com/recipes/recipes-a-z/'
    page = requests.get(url) 
    soup = BeautifulSoup(page.content, "html.parser")

    # Create empty list to store a master list of all recipe urls on Food Network
    master_urls = []

    # Find the section of each page that contains the recipe urls
    box = soup.find('div', class_='l-Columns l-Columns--2up')

    # Filter for all the specific links of the recipe urls
    result = box.find_all('a', href=True)

    # Store just the urls into the master list
    for link in result:
        master_urls.append(link['href'])

    # Clean up master list to remove prefix "//"
    master_urls = list(map(lambda x: str(x).replace('//', ''), master_urls))

    # Gather index of urls and number of pages for each url
    index = ['123', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'xyz']
    total_pages = {}
    root = 'https://www.foodnetwork.com/recipes/recipes-a-z/'

    threads = []
    for i in index:
        t = threading.Thread(target=get_page_count, args=(root, i, total_pages))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()

    print("Done!")

    print(total_pages)

    ingredients_to_include = event.get('include', [])
    ingredients_to_exclude = event.get('exclude', [])

    return {
        'statusCode': 200,
        'body': json.dumps(total_pages)
    }


def get_page_count(root, i, total_pages):
        
    last_page = False
    pg = 1
    while not last_page:
        print("Scraping page {}-{}".format(i, pg))
        
        page_url = f'{root}/{i}/p/{pg}'
        visit_page_url = requests.get(page_url)
        soup_page = BeautifulSoup(visit_page_url.content, "html.parser")
        next_button = str(soup_page.select('a[class*="o-Pagination__a-NextButton"]')) 
        if "o-Pagination__a-NextButton is-Disabled" in next_button:
            last_page = True 
        else:
            pg += 1
    total_pages[i] = pg
    
if __name__ == "__main__":
    response = lambda_handler({
        "include": [],
        "exclude": ["milk", "butter", "garlic", "broccoli", "onions", "cauliflower", "peanuts"]
    }, {})



    # print(response["body"])

    # print(master_urls)

    ######################

    # index_ = ['123', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'xyz']
    # total_pages_ = {}
    # root_ = 'https://www.foodnetwork.com'
    # for i in index_:
    #     last_page_ = False
    #     pg_ = 1
    #     while not last_page:
    #         page_url_ = f'{root}/{i}/p/{pg}'
    #         visit_page_url_ = requests.get(page_url_)
    #         soup_page_ = BeautifulSoup(visit_page_url_.content, "html.parser")
    #         next_button_ = str(soup_page_.select('a[class*="o-Pagination__a-NextButton"]')) 
    #         if "o-Pagination__a-NextButton is-Disabled" in next_button_:
    #             total_pages_[i] = pg    
    #             last_page_ = True 
    #         else:
    #             pg_ += 1

    # print(total_pages_)

    # Find out how many pages each url has
    # n_pages = 0
    # test_url = "https://www.foodnetwork.com/recipes/recipes-a-z/xyz/p/4"
    # test = requests.get(test_url)
    # soup2 = BeautifulSoup(test.content, "html.parser")
    # navigation = soup2.find('section', class_='o-Pagination')
    # next_button = str(navigation.select('a[class*="o-Pagination__a-NextButton"]'))
    # last_page = False
    # if "o-Pagination__a-NextButton is-Disabled" in next_button:
    #     last_page = True

    # print(next_button)
    # print(last_page)


    # Iterate through every page of a url
    # Repeat the master_url recursive formula
    # Enter each url in the master_urls list and investigate...
        # Another recursive formula to inspect the ingredients box on each recipe to see if it contains INCLUDED list AND excludes the EXCLUDED list
        # If true, add to new list, results_urls








    # content = result.text
    # soup = BeautifulSoup(content, 'lxml')
    # print(soup.prettify())

    # box = soup.find('div', class_='l-Columns l-Columns--2up')

    # master_urls = []

    # for link in box.find_all('a', href=True):
    #     master_urls.append(link['href'])

    # print(master_urls)

    # At each page of a-z list, collect all urls to recipes and store in MasterList
    

    # Iterate over each sub page of a-z list and do the same as above
    # Read through every recipe url in MasterList
        # For every recipe where ingredients contains items in INCLUDE list and does not contain items in EXXCLUDE list, store to recipe_urls





       # recipe_urls = []

    # website = 'https://www.foodnetwork.com/recipes/recipes-a-z/'
    # result = requests.get(website)




    # content = result.text
    # soup = BeautifulSoup(content, 'lxml')

    # root = 'https://www.foodnetwork.com/recipes/recipes-a-z/'
    # website = f'{root}/recipes'
    # box = soup.find('span', class_='o-AssetTitle__a-HeadlineText')
    # box.find_all('a', href=True)

    # links = [link['href'] for link in box.find_all('a', href=True)]
    
    # for link in links:
    #     result = requests.get(f'{root}/{link}')
    #     content = result.text
    #     soup = BeautifulSoup(content, 'lxml')

    # # Define the list of recipe websites to scrape
    # recipe_websites = [
    #     'https://www.foodnetwork.com/'
    # ]

    # for website in recipe_websites:
    #     response = requests.get(website)
    #     soup = BeautifulSoup(response.content, 'html.parser')

    #     # Scrapin
    #     # Modify this logic to match the structure of the websites you'reg logic to find links to recipe subpages scraping
    #     recipe_links = [link['href'] for link in soup.find_all('li', class_='m-PromoList__a-ListItem')]

    #     # Iterate through each recipe link and scrape its content
    #     for link in recipe_links:
    #         recipe_url = website + link  # Construct the full URL of the recipe subpage
    #         recipe_response = requests.get(recipe_url)
    #         recipe_soup = BeautifulSoup(recipe_response.content, 'html.parser')

    #         # Extract recipe information
    #         recipe_ingredients = [ingredient.text for ingredient in recipe_soup.find_all('span', class_='o-Ingredients__a-Ingredient--CheckboxLabel')]
            
    #         # Check if the recipe includes all ingredients to include and excludes all ingredients to exclude
    #         if all(ingredient in recipe_ingredients for ingredient in ingredients_to_include) \
    #                 and not any(ingredient in recipe_ingredients for ingredient in ingredients_to_exclude):
    #             recipe_urls.append(recipe_url)
    
    #     # Return the list of recipe URLs
    # return {
    #     'statusCode': 200,
    #     'body': json.dumps(recipe_urls)
    # }
    
    # Scrape websites for recipes that include and exclude certain items
    # Output recipe urls for user
    # print("hello, world")
    # print(event)
    # body = json.loads(event["body"])
    # value1 = body["value1"]
    # return {
    #     'statusCode': 200,
    #     'body': json.dumps(value1 + 1)
    # }