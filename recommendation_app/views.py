import os
import pandas as pd
import numpy as np
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import string
import random
from neo4j import GraphDatabase
from manage import driver
from datetime import date 



"""    Utility functions    """
class Product:
    def __init__(self, productid, productname, manufacturer, style, finish, category, price, poster):
        self.productid = productid
        self.productname = productname
        self.manufacturer = manufacturer
        self.style = style
        self.finish = finish
        self.category = category
        self.price = price
        self.poster = poster

    def as_dict(self):
        return {'productid': self.productid, 'productname': self.productname, 'manufacturer': self.manufacturer, 'style': self.style, 
            'finish': self.finish, 'category': self.category, 'price': self.price, 'poster': self.poster}

class Category:
    def __init__(self, category, poster):
        self.category = category
        self.poster = poster

    def as_dict(self):
        return {'category': self.category, 'poster': self.poster}   

class CategoryRollUp:
    def __init__(self, categoryrollup, poster):
        self.categoryrollup = categoryrollup
        self.poster = poster

    def as_dict(self):
        return {'categoryrollup': self.categoryrollup, 'poster': self.poster}           


def set_product(x):
    return Product(x.ProductId, x.ProductName, x.Manufacturer, x.Style, x.Finish, x.Category, x.Price, x.Poster)


def set_categoryrollup(x):
    return CategoryRollUp(x.CategoryRollUp, x.Poster)

def compare(smaller, bigger):
    smaller = str(smaller).translate(str.maketrans('', '', string.punctuation+" ")).lower()
    bigger = str(bigger).translate(str.maketrans('', '', string.punctuation+ " ")).lower()
    return smaller in bigger

def search_products(search_type, search_key):

    if search_type == 'All':
        query = '''match(p:Product)<-[:HasProduct]-(c)
        where toLower(p.ProductName) contains toLower("'''+str(search_key)+'''") or toLower(p.Manufacturer) contains toLower("'''+str(search_key)+'''") or toLower(p.Style) contains toLower("'''+str(search_key)+'''") or toLower(p.Finish) contains toLower("'''+str(search_key)+'''") or toLower(c.Category) contains toLower("'''+str(search_key)+'''")
        RETURN  toString(p.ProductId) as id, p.ProductName as ProductName, p.Manufacturer as Manufacturer, p.Style as Style, p.Finish as Finish, c.Category as Category, p.Price as Price, p.poster as Poster limit 12'''
    
    elif search_type == 'Product':
        query = '''match(p:Product)<-[:HasProduct]-(c)
        where toLower(p.ProductName) contains toLower("'''+str(search_key)+'''") 
        RETURN  toString(p.ProductId) as id, p.ProductName as ProductName, p.Manufacturer as Manufacturer, p.Style as Style, p.Finish as Finish, c.Category as Category, p.Price as Price, p.poster as Poster limit 12'''
    
    elif search_type == 'Manufacturer':
        query = '''match(p:Product)<-[:HasProduct]-(c)
        where toLower(p.Manufacturer) contains toLower("'''+str(search_key)+'''") 
        RETURN  toString(p.ProductId) as id, p.ProductName as ProductName, p.Manufacturer as Manufacturer, p.Style as Style, p.Finish as Finish, c.Category as Category, p.Price as Price, p.poster as Poster limit 12'''

    elif search_type == 'Category':
        query = '''match(p:Product)<-[:HasProduct]-(c)
        where toLower(c.Category) contains toLower("'''+str(search_key)+'''")
        RETURN  toString(p.ProductId) as id, p.ProductName as ProductName, p.Manufacturer as Manufacturer, p.Style as Style, p.Finish as Finish, c.Category as Category, p.Price as Price, p.poster as Poster limit 12'''

       
    try:
        product_frame = pd.DataFrame(driver.session().run(query))
        print('%%%%%%%')
        
        product_frame.columns = ['ProductId' ,'ProductName', 'Manufacturer','Style','Finish','Category','Price','Poster']
        print(product_frame)
        product_list = list(product_frame.apply(set_product, axis=1))
    
       
        return product_list
       
    except: 
        return []
        

def recommendation_algo_one(key):
    query = '''MATCH (p:Product)
        where p.ProductId ="'''+str(key)+'''"
        WITH p
        match(p1:Product{SubCategory:p.SubCategory})<-[:HasProduct]-(c:Category) where p<>p1
        with p,p1,c,apoc.text.sorensenDiceSimilarity(p.ProductName, p1.ProductName) as sim order  by sim desc
        RETURN  toString(p1.ProductId) as id, p1.ProductName as ProductName, p1.Manufacturer as Manufacturer, p1.Style as Style, p1.Finish as Finish, c.Category as Category,p1.Price as Price, p1.poster as Poster limit 6'''

    product_frame = pd.DataFrame(driver.session().run(query))
    
    if(len(product_frame) == 0):
        return('Empty')
    
    product_frame.columns = ['ProductId' ,'ProductName', 'Manufacturer','Style','Finish','Category','Price','Poster']
    product_list = list(product_frame.apply(set_product, axis=1))
    return product_list
def recommendation_algo_one(key):
    query = '''MATCH (p:Product)
        where p.ProductId ="'''+str(key)+'''"
        WITH p
        match(p1:Product{SubCategory:p.SubCategory})<-[:HasProduct]-(c:Category) where p<>p1
        with p,p1,c,apoc.text.sorensenDiceSimilarity(p.ProductName, p1.ProductName) as sim order  by sim desc
        RETURN  toString(p1.ProductId) as id, p1.ProductName as ProductName, p1.Manufacturer as Manufacturer, p1.Style as Style, p1.Finish as Finish, c.Category as Category,p1.Price as Price, p1.poster as Poster limit 6'''

    product_frame = pd.DataFrame(driver.session().run(query))
    
    if(len(product_frame) == 0):
        return('Empty')
    
    product_frame.columns = ['ProductId' ,'ProductName', 'Manufacturer','Style','Finish','Category','Price','Poster']
    product_list = list(product_frame.apply(set_product, axis=1))
    return product_list


def recommendation_algo_two(key):
    query = '''MATCH (p:Product)
        where p.ProductId ="'''+str(key)+'''"
        WITH p
        match(p1:Product{SubCategory:p.SubCategory})<-[:HasProduct]-(c:Category) where p<>p1
        with p,p1,c,apoc.text.sorensenDiceSimilarity(p.ProductName, p1.ProductName) as sim order  by sim desc
        RETURN  toString(p1.ProductId) as id, p1.ProductName as ProductName, p1.Manufacturer as Manufacturer, p1.Style as Style, p1.Finish as Finish, c.Category as Category,p1.Price as Price, p1.poster as Poster limit 6'''

    product_frame = pd.DataFrame(driver.session().run(query))
    
    if(len(product_frame) == 0):
        return('Empty')
    
    product_frame.columns = ['ProductId' ,'ProductName', 'Manufacturer','Style','Finish','Category','Price','Poster']
    product_list = list(product_frame.apply(set_product, axis=1))
    return product_list


def recommendation_algo_three(key):
    query = '''MATCH (p:Product)
        where p.ProductId ="'''+str(key)+'''"
        WITH p
        match(p1:Product{SubCategory:p.SubCategory})<-[:HasProduct]-(c:Category) where p<>p1
        with p,p1,c,apoc.text.sorensenDiceSimilarity(p.ProductName, p1.ProductName) as sim order  by sim desc
        RETURN  toString(p1.ProductId) as id, p1.ProductName as ProductName, p1.Manufacturer as Manufacturer, p1.Style as Style, p1.Finish as Finish, c.Category as Category,p1.Price as Price, p1.poster as Poster limit 6'''

    product_frame = pd.DataFrame(driver.session().run(query))
    
    if(len(product_frame) == 0):
        return('Empty')
    
    product_frame.columns = ['ProductId' ,'ProductName', 'Manufacturer','Style','Finish','Category','Price','Poster']
    product_list = list(product_frame.apply(set_product, axis=1))
    return product_list

@csrf_exempt
def home(request):
    
    query = '''match(h:CategoryRollUp)
    with collect(h) as v
    unwind v as c
    match(c)-[:HasCategory]->(d)-[:HasProduct]->(p)
    with c,collect(p) as k
    with c,k
    unwind k[..1]  as l
    return c.CategoryRollUp,l.poster'''
    categoryrollup_frame = pd.DataFrame(driver.session().run(query))
    categoryrollup_frame.columns = ['CategoryRollUp','Poster']
    categoryrollup_list = list(categoryrollup_frame.head(10).apply(set_categoryrollup, axis=1))
    #print(categoryrollup_frame)
    title = "Top 5 products"
    search_type, search_key = 'All', ''
    if request.method == 'POST':
        search_type = request.POST['search_type']
        search_key = request.POST['search_key']
        if len(search_key) > 0:
            title = 'Search results for {} in category {}'.format(search_key, search_type)
            product_list = search_products(search_type, search_key)
        print('######################################################')
        print(product_list)    
        context = {
        'products':product_list,
        'title':title,
        'search_key':search_key,
        'search_type':search_type,
        'radios': 'All Product Manufacturer Category'.split()
        }
        return render(request, 'neo4j/search.html', context)
    #print("Showing {} results".format(len(movie_list)))
    context = {
        'categoryrollup':categoryrollup_list,
        'title':title,
        'search_key':search_key,
        'search_type':search_type,
        'radios': 'All Product Manufacturer Category'.split()
    }
    #print(context)
    return render(request, 'neo4j/index.html', context)

@csrf_exempt
def detail(request, key):
    query = '''match(p1:Product)<-[:HasProduct]-(c:Category)
    where p1.ProductId = "'''+str(key)+'''"
    RETURN  toString(p1.ProductId) as id, p1.ProductName as ProductName, p1.Manufacturer as Manufacturer, p1.Style as Style, p1.Finish as Finish, c.Category as Category,p1.Price as Price, p1.poster as Poster limit 6'''
    
    product_frame = pd.DataFrame(driver.session().run(query))
    print('%%%%%%%')
    
    product_frame.columns = ['ProductId' ,'ProductName', 'Manufacturer','Style','Finish','Category','Price','Poster']
    print(product_frame)
    product_frame.index = [0]
    
    
    
    context = {
        'products': set_product(product_frame.loc[0]),
        'algo_one': recommendation_algo_one(key),
        'algo_two': recommendation_algo_one(key),
        'algo_one': recommendation_algo_one(key),
        'search_key':"",
        'search_type': 'All',
        'radios': 'All Product Manufacturer Category'.split()
        
    }
    
    context['PAGE_NAME'] = context['products'].productname
    

    return render(request, 'neo4j/detail.html', context)