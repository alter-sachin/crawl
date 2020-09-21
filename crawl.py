import requests
import sys
import os
import json

sys.path.append("../beautifulsoup4-4.9.0")

import bs4

#base_url = "https://www.levi.in/new_arrivals"
#page = requests.get(base_url)
#soup = BeautifulSoup(page.content, 'html.parser')

#https://www.levi.in/new_arrivals?start=0&sz=12&format=page-element
base_url = "https://www.levi.in/new_arrivals"
url_list = 	[	"http://www.levi.in/",
			"http://www.levi.in/",
			"http://www.levi.in/",
			"http://www.levi.in/",
		]
save_dir = "./temp"

OUTPUT_FILE = 'output.json'

class crawl_out():
	def __init__(self, name, img_main, imgs, num, price, colors, desc, categories, fit_descs, material_descs):
		self.name = name
		self.img_main = img_main
		self.imgs = imgs
		self.num = num
		self.price = price
		self.colors = colors
		self.desc = desc
		self.categories = categories
		self.fit_descs = fit_descs
		self.material_descs = material_descs

def create_soup(url,iter):
	size=12
	pagination_url = base_url + "?start="+str(iter*size)+"&sz="+str((iter+1)*size)+"&format=page-element"
	page = requests.get(pagination_url)
	soup = bs4.BeautifulSoup(page.content, 'html.parser')
	return soup

def retrieve_all_products(soup):
	all_products = soup.find_all('li',class_='grid-tile')
	return all_products

def productpage_crawl(product_page):
	page = requests.get(product_page)
	soup = bs4.BeautifulSoup(page.content,'html.parser')

	temp = soup.find("h1", class_="product-name")
	if(type(temp) == bs4.element.Tag):
		name = temp.text
	else:
		name = ""

	temp = soup.find("img", class_="product-image")
	if(type(temp) == bs4.element.Tag):
		img1 = temp.get("src")
	else:
		img1 = ""
	imgs_rest = soup.find_all("li", class_="product-image")

	imgs = list();

	for img in imgs_rest:
		temp = img.find("img")
		if(type(temp) == bs4.element.Tag):
			imgs.append(temp.get("src"))

	temp = soup.find("span", class_="item-number")
	if(type(temp) == bs4.element.Tag):
		product_num = temp.text
	else:
		product_num = ""
	temp = soup.find("div", class_="product-price").find("span", class_="pricevalue")
	if(type(temp) == bs4.element.Tag):
		product_price = temp.text[1:]
	else:
		product_price = ""

	colors_list = soup.find("ul", class_="swatches").find_all("li", class_="selectable")

	colors = list();

	for color in colors_list:
		temp = color.find("a")
		if(type(temp) == bs4.element.Tag):
			colors.append(temp.get("title")[14:])

	temp = soup.find("meta", attrs={"name":"keywords"})
	if(type(temp) == bs4.element.Tag):
		categories = temp.get('content').split(',')

	for i in range(len(categories)):
		categories[i] = categories[i].strip()

	temp = soup.find("td", class_="product-details").find("div", class_="tab-content")
	if(type(temp) == bs4.element.Tag):
		desc = temp.text

	fit_list = soup.find("td", class_="fit-and-size").find_all("li")
	fit_descs = list();

	for fit in fit_list:
		if(type(fit) == bs4.element.Tag):
			fit_descs.append(fit.text)

	material_list = soup.find("td", class_="product-material").find_all("li")
	material_descs = list();

	for material in material_list:
		if(type(material) == bs4.element.Tag):
			material_descs.append(material.text)

	return crawl_out(name, img1, imgs, product_num, product_price, colors, desc, categories, fit_descs, material_descs)

if __name__=='__main__':

	out_file = open(OUTPUT_FILE, "w")

	pages = 2
	for x in range(0,pages):
		soup = create_soup(base_url,x)
		products = retrieve_all_products(soup)
		print("Gathering batch: ", len(products))

		product_details = []
		for product in products:
			#new_soup = BeautifulSoup(product,'html.parser')
			#print(product)
			img_url = product.find("a", class_="name-link")
			if(type(img_url) != bs4.element.Tag):
				print("Skipping an image. No url found")
				continue

			product_page = (base_url + img_url['href'])
			out = productpage_crawl(product_page)

			if len(out.categories) == 0 or out.categories[0] == "" or out.name == "":
				print("Error in a crawl operation")
			else:
				print("Writing ", out.name, " in category ", out.categories[0],
					" and ", out.categories[1])

			for category in out.categories[0:1]:
				str_save = json.dumps(	{
						'category' : category,
						'name' : out.name,
						'price' : out.price,
						'item_num' : out.num,
						'colors' : out.colors,
						'desc' : out.desc,
						'image-main' : out.img_main,
						'image-others' : out.imgs,
						'fit-info' : out.fit_descs,
						'material-info' : out.material_descs
					}, indent = 4)
				out_file.write(str_save)

	out_file.close()
