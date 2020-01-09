from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
import geocoder
import urllib.request, urllib.parse
import requests
import json
import math


db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    uid = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    pwdhash = db.Column(db.String(54))

    def __init__(self, firstname, lastname, email, password):
        self.firstname = firstname.title()
        self.lastname = lastname.title()
        self.email = email.lower()
        self.set_password(password)

    def set_password(self,password):
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)

# p = Place()
# places = p.query("1600 Amphitheater Parkway Mountain View CA")
class Place(object):
    def meters_to_walking_time(self, meters):
    # 80 meters is one minute walking time
        return int(meters / 80)

    def wiki_path(self, slug):
        return urllib.parse.urljoin("http://en.wikipedia.org/wiki/", slug.replace(' ', '_'))

    def address_to_latlng(self, address):
        g = geocoder.google(address, key='AIzaSyA5AI-rtN9Ezzh4NWacGF7wNyyyBIgGVII')
        return (g.lat, g.lng)

    def query(self, address):
        lat, lng = self.address_to_latlng(address)
        query_url = 'https://en.wikipedia.org/w/api.php?action=query&list=geosearch&gsradius=5000&gscoord={0}%7C{1}&gslimit=20&format=json'.format(lat, lng)
        g = urllib.request.urlopen(query_url)
        results = g.read()
        g.close()

        data = json.loads(results)

        #temp = json.dumps(data)
        places = []
        for place in data['query']['geosearch']:
            name = place['title']
            meters = place['dist']
            lat = place['lat']
            lng = place['lon']

            wiki_url = self.wiki_path(name)
            walking_time = self.meters_to_walking_time(meters)

            d = {
            'name': name,
            'url': wiki_url,
            'time': walking_time,
            'lat': lat,
            'lng': lng
            }
            places.append(d)

        return places

class Categories(object):
    def return_categories(self):
        url = 'https://api2.shop.com/AffiliatePublisherNetwork/v2/categories?publisherId=5c3624328adc4b7b96f64d06c59daa91&locale=en_GB&site=shop&shipCountry=GB&onlyMaProducts=false'

        hdr = {'accept': 'application/json', 'api_Key':'5c3624328adc4b7b96f64d06c59daa91'
        }

        req = urllib.request.Request(url,None,hdr)
        response = urllib.request.urlopen(req).read().decode('utf8')

        data = json.loads(response)

        categories = []
        for cat in data['categories']:
            temp = []
            cat_id = cat['id']
            cat_links = cat['links']
            cat_href = cat_links[0]['href']
            cat_rel = cat_links[0]['rel']
            category = cat['name']
            c = {
            'cat_id': cat_id,
            'link': cat_href,
            'rel': cat_rel,
            'category': category
            }
            temp.append(c)
            for sub in cat['subCategories']:
                sub_id = sub['id']
                sub_links = sub['links']
                sub_href = sub_links[0]['href']
                sub_rel = cat_links[0]['rel']
                subcat = sub['name']
                s = {
                'sub_id': sub_id,
                'link': sub_href,
                'rel': sub_rel,
                'subcat': subcat
                }
                temp.append(s)

            categories.append(temp)

        return categories

class Products(object):
    def search_query(self, query, cat_id):
        search_term = urllib.parse.quote(query)
        if cat_id == "placeholder":
            cat_id = ""
        else:
            cat_id = "&categoryId=" + cat_id

        url = 'https://api2.shop.com/AffiliatePublisherNetwork/v2/products?publisherId=5c3624328adc4b7b96f64d06c59daa91&locale=en_GB&site=shop&shipCountry=GB&term={0}&start=0&perPage=48{1}&onlyMaProducts=false'.format(search_term, cat_id)

        hdr = {'accept': 'application/json', 'api_Key':'5c3624328adc4b7b96f64d06c59daa91'
        }

        req = urllib.request.Request(url,None,hdr)
        response = urllib.request.urlopen(req).read().decode('utf8')

        data = json.loads(response)

        product_count = data['numberOfProducts']
        pages = {'productPages' : math.ceil(product_count / 48)}

        products = []
        for item in data['products']:
            name = item['image']['caption']
            image = item['image']['sizes'][1]['url']
            price = item['maximumPrice']
            desc = item['shortDescription']
            id = item['id']

            d = {
            'name': name,
            'image': image,
            'price': price,
            'description': desc,
            'id': id
            }
            products.append(d)

        products.append(pages)

        return products

class Product_details(object):
    def return_product(self, product_id):

        url = 'https://api2.shop.com/AffiliatePublisherNetwork/v2/products/{0}?publisherId=5c3624328adc4b7b96f64d06c59daa91&locale=en_GB&site=shop&shipCountry=GB'.format(product_id)

        hdr = {'accept': 'application/json', 'api_Key':'5c3624328adc4b7b96f64d06c59daa91'
        }

        req = urllib.request.Request(url,None,hdr)
        response = urllib.request.urlopen(req).read().decode('utf8')

        data = json.loads(response)

        for each in data:
            print(each)

        return data
