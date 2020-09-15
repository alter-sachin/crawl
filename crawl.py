from bs4 import BeautifulSoup
import requests
import os
#base_url = "https://www.levi.in/new_arrivals"
#page = requests.get(base_url)
#soup = BeautifulSoup(page.content, 'html.parser')

#https://www.levi.in/new_arrivals?start=0&sz=12&format=page-element
base_url = "https://www.levi.in/new_arrivals"
save_dir = "./temp"


def create_soup(url,iter):
	size=12
	pagination_url = base_url + "?start="+str(iter*size)+"&sz="+str((iter+1)*size)+"&format=page-element"
	page = requests.get(pagination_url)
	soup = BeautifulSoup(page.content, 'html.parser')
	return soup

def retrieve_all_products(soup):
	all_products = soup.find_all('li',class_='grid-tile')
	print(len(all_products))
	return all_products

def save_attributes(img, name, desc):
	file = os.open("w", save_dir + name + ".txt")
	os.write(file, name + "\n" + desc)
	os.close(file)
	file = os.open("w", save_dir + name + ".jpg")
	os.write(file, img)
	os.close(file)

def productpage_crawl(product_page):
	page = requests.get(product_page)
	soup = BeautifulSoup(page.content,'html.parser')

	link = soup.find("div", class_="product_primary_image").find("img").src
	img = requests.get(link)

	name = soup.find("h1", class_="product-name").text
	desc = soup.find("td", class_="product_details").find("div", class_="tab_content").text

	save_attributes(img, name, desc);

if __name__=='__main__':
	pages = 10
	for x in range(0,pages):
		soup = create_soup(base_url,x)
		products = retrieve_all_products(soup)
		#print(products)
		
		product_details = []
		for product in products:
			#new_soup = BeautifulSoup(product,'html.parser')
			#print(product)
			product_name = product.find("div",class_="product-name")
			print(product_name.text)
			product_price = product.find("div",class_="product-pricing")
			print(product_price.text)
			product_img = product.find("div",class_="product-image")
			img_url =  product_img.find('a',href=True)
			product_page = (base_url + img_url['href'])
			productpage_crawl(product_page)
