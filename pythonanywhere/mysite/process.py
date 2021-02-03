import pymysql
import re

from VariableByteEncoder import *
import json
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
app = Flask(__name__)
app.config.from_object(__name__)
CORS(app,resources={r'/*': {'origins': '*'}})

@app.route('/')
def index():
    return render_template('index.html')


def getweather1(latitude ,longitude):
    import json
    from urllib import request
    temparray = []


    #darksky
    keyid = 'eb3cb3d158c5a78a3288451c725f618a'
    url = "https://api.darksky.net/forecast/"+keyid+"/"+latitude+","+longitude
    response = request.urlopen(url)
    str_response = response.read().decode('utf-8')
    data = json.loads(str_response)
    celsius = int(((int(data["currently"]["temperature"])-32)*5)/9)
    #celsius = data["currently"]["temperature"]
    present_status = data["currently"]["icon"]
    future_status = data["minutely"]["icon"]
    #text = "accurate temperature in your area "+cityname+","+countryname+" is "+str(celsius)+"C and may be "+str(data["currently"]["summary"])
    temparray.append(celsius)
    #return text
    avgtemp = sum(temparray)/len(temparray)

    #degree_sign = '\u00b0'
    #text = "accurate temperature in your area "+cityname+","+countryname+" is "+str(avgtemp)+degree_sign+"C"
    return avgtemp,present_status,future_status

def getlocation(ip):
    import pygeoip
    dataname = pygeoip.GeoIP(r'/home/ttsheng/mysite/GeoLiteCity.dat')
    data = dataname.record_by_name(ip)
    country = data['country_name']
    city = data['city']
    longi = data['longitude']
    lat = data['latitude']
    return str(city),str(country),str(lat),str(longi)



#for getting ip
def getip_test():
    import json
    from urllib import request
    url = 'http://ipinfo.io/json?ca'
    response = request.urlopen(url)
    str_response = response.read().decode('utf-8')
    data1 = json.loads(str_response)
    IP=data1['ip']
    region = data1['region']
    return IP
def gettemplist(temp_list):
    list1 = []
    db = pymysql.connect("ttsheng.mysql.pythonanywhere-services.com","ttsheng","bft8299py","ttsheng$recipes" )
    cursor = db.cursor()
    format_strings = ','.join(['%s'] * len(temp_list))
    cursor.execute("SELECT recipe_ids FROM ingredient_index WHERE ingredient IN (%s)" %format_strings,tuple(temp_list))
    results = cursor.fetchall()
    for row in results:
        list1 += decode(row[0])
    return list1
@app.route("/getip")
def getip():
    from nltk.stem import PorterStemmer
    ps = PorterStemmer()
    #city,country,lat,long = getlocation(request.remote_addr)
    db = pymysql.connect("ttsheng.mysql.pythonanywhere-services.com","ttsheng","bft8299py","ttsheng$recipes" )
    cursor = db.cursor()
    from datetime import datetime
    args = request.args
    #print(args['time'])
    today1 = datetime.fromisoformat(args['time'].replace('Z',''))
    today = today1.date().strftime("%Y-%m-%d")
    time = today1.strftime("%H")
    if int(time)>=0 and int(time)<=11:
        time_message = "Good Morning! "
    elif int(time)>=12 and int(time)<=15:
        time_message = "Good Afternoon! "
    elif int(time)>=16 and int(time)<=24:
        time_message = "Good Evening! "
    sql = ("""SELECT Celebration,Message FROM celebration_calendar WHERE date LIKE %s""", today)
    cursor.execute(*sql)
    celebration = cursor.fetchall()
    #print(celebration,today)
    if len(celebration)==0:
        try:
            city,country,lat,long = getlocation(request.environ.get('HTTP_X_REAL_IP', request.remote_addr))
            #city,country,lat,long = getlocation(request.remote_addr)
            temp,present_status,future_status = getweather1(lat,long)
            snow_factors = ['snow','fog','sleet']
            rain_factors = ['rain']
            clear_factors = ['clear-day','clear-night']
            cloudy_factors = ['cloudy','partly-cloudy-day','partly-cloudy-night']
            wind_factors = ['wind']
            snow,rain,clear,cloud,wind = False,False,False,False,False
            if present_status in snow_factors:
                snow = True
                mess = " snowy "
            elif present_status in rain_factors:
                rain = True
                mess = " rainy "
            elif present_status in clear_factors:
                clear = True
                mess = " pleasant "
            elif present_status in cloudy_factors:
                cloud = True
                mess = " cloudy "
            elif present_status in wind_factors:
                wind = True
                mess = " windy "
            json_dict = {'recipe_info':[],'message':"",'length':"",'weather':1}
            if int(temp)<=10:
                temp_list = [ps.stem('summer'),ps.stem('chilled'),ps.stem('ice'),ps.stem('salad')]
                json_dict['recipe_info'] = gettemplist(temp_list)

                json_dict['message'] = time_message+"Welcome culinary chef! Its seems cold and"+mess+"at your location. How about some warm recipes"
                json_dict['length'] = len(json_dict['recipe_info'])
            elif  int(temp)>10 and int(temp)<=20:
                temp_list = [ps.stem('spring')]
                json_dict['recipe_info'] = gettemplist(temp_list)
                json_dict['message'] = time_message+"Welcome culinary chef! Temperature seems normal and"+mess+"at your location. Here is our suggestions"
                json_dict['length'] = len(json_dict['recipe_info'])
            elif int(temp)>20:
                temp_list = [ps.stem('winter'),ps.stem('autumn'),ps.stem('hot'),ps.stem('warm')]
                json_dict['recipe_info'] = gettemplist(temp_list)
                json_dict['message'] = time_message+"Welcome culinary chef! Temperature seems hot and"+mess+"at your location. How about some cold recipes"
                json_dict['length'] = len(json_dict['recipe_info'])
            #print("success temp",json_dict)
            return json.dumps(json_dict)
        except:
            temp_list = [ps.stem('spring')]
            json_dict['recipe_info'] = gettemplist(temp_list)
            json_dict['message'] = "Welcome culinary chef! Here are our suggestions for the day"

    else:
        json_dict = {'recipe_info':[],'weather':0,'message':"",'length':""}
        counter = 0
        for row in celebration:
            message = row[1]
            sql = ("""SELECT recipe_ids FROM ingredient_index WHERE ingredient LIKE %s""", ps.stem(row[0]))
            cursor.execute(*sql)
            results = cursor.fetchall()
            recipe_id_list = []
            for row1 in results:
                recipe_id_list += decode(row1[0])
        mess = time_message+"Welcome culinary chef! "
        json_dict['recipe_info'] = recipe_id_list
        json_dict['message'] = mess+message
        json_dict['length'] = len(recipe_id_list)
        return json.dumps(json_dict)
        """
                for id in recipe_id_list:
                    sql = (""""SELECT image_url,description, recipe_url, title FROM recipe_info WHERE recipe_id LIKE %s"""",id)
                    cursor.execute(*sql)
                    results2 = cursor.fetchall()
                    for row2 in results2:
                        image_url = row2[0]
                        desc = row2[1]
                        recipe_url = row2[2]
                        title = row2[3]
                        desc = desc.replace('None',"")
                        if ('None' in image_url and desc == ""):
                            continue
                        counter +=1
                        print(image_url,desc,recipe_url,title)
                        if counter >9:
                            print(json_dict)
                            return json.dumps(json_dict)
                        json_dict['recipe_info'].append({'id':id,'src':image_url,'desc':desc,'title':title,'url':recipe_url})
        return json_dict"""






@app.route("/test")
def test():
    from nltk.stem import PorterStemmer
    import time
    ps = PorterStemmer()
    args = request.args
    #return json.dumps({'data':"gotit "+str(args['city'])})
    start = time.time()
    # Open database connection
    db = pymysql.connect("ttsheng.mysql.pythonanywhere-services.com","ttsheng","bft8299py","ttsheng$recipes" )
    #db = pymysql.connect("shareddb-r.hosting.stackcp.net","tingsheng","ts123123","recipes-3132330cb1" )
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    #ip,region = getip()
    #print(region,getlocation(ip))
    if args['city'].lower():
        import sys
        #from itertools import permutations
        #query = ' '.join(sys.argv[1:])
        query = args['city']
        query = re.split(r'[, - : ; + ! @ # $ ^ & * . " \' { } | \s+ ]+',query.strip())
        window_frame = len(query)
        query_append = []
        while window_frame>=1:
            for i in range(len(query)):
                if i < window_frame:
                    query_append.append(" ".join(query[i:window_frame]))
            window_frame -=1
        query = query_append
        #print(query)



        recipe_dict = dict()
        query_list = []
        for word in query:
            query_list.append(str(ps.stem(word.lower())))
            #word = PorterStemmer().stem(word)
        format_strings = ','.join(['%s'] * len(query_list))
        #query_str = "("+query_str+")"
        #print(query_list)
        #sql = "SELECT recipe_ids FROM ingredient_index WHERE ingredient IN (%s)".format(query_str)
        cursor.execute("SELECT synonym FROM synonym_table WHERE ingredient IN (%s)" %format_strings,tuple(query_list))
        results = cursor.fetchall()
        synonym = []
        for row in results:
            synonym += row[0].strip().split(',')
        query_list += synonym
        #print(query_list)
        format_strings = ','.join(['%s'] * len(query_list))
        cursor.execute("SELECT recipe_ids FROM ingredient_index WHERE ingredient IN (%s)" %format_strings,tuple(query_list))
        results = cursor.fetchall()
        if len(results)==0:
                #sys.exit(1)
            return json.dumps({'id':[],'length':0,'error':1,'message':"Sorry! The Ingredient does not seem familiar. But here are some suggestions from our side"})
        for row in results:
            recipe_id_list = decode(row[0])
            for recipe_id in recipe_id_list:
                if recipe_id not in recipe_dict:
                    recipe_dict[recipe_id] = 1
                else:
                    recipe_dict[recipe_id] +=1

        recipe_common_ing_count = {}
        recipe_sql_list = []
        error = None
        for recipe in recipe_dict.keys():
            if recipe_dict[recipe] > 1 or len(query)==1:
                recipe_sql_list.append(recipe)
        if len(recipe_sql_list)==0:
            error = 3
            recipe_sql_list = list(recipe_dict.keys())
        format_strings = ','.join(['%s'] * len(recipe_sql_list))
        #sql = ("""SELECT recipe_id,ingredient_count FROM recipe_info WHERE recipe_id IN %s""", recipe)
        cursor.execute("SELECT recipe_id,ingredient_count FROM recipe_info WHERE recipe_id IN (%s)" %format_strings,tuple(recipe_sql_list))
        results = cursor.fetchall()
        for row in results:
            recipe_common_ing_count[row[0]] = int(row[1])-recipe_dict[row[0]]

        shopping_hungryparams = args['shopping_hungry'].strip().split(',')
        very_hungry_param = False
        shopping_param = False
        for param in shopping_hungryparams:
            if 'hungry' in param.lower():
                very_hungry_param = True
            if 'shopping' in param.lower():
                shopping_param = True
        #print(shopping_param,very_hungry_param)

        checkbox = args['checkbox'].strip()
        checkbox_ing = checkbox.split(",")
        checkbox_ing = [x.lower() for x in checkbox_ing]
        format_strings = ','.join(['%s'] * len(checkbox_ing))
        cursor.execute("SELECT recipe_ids FROM ingredient_index WHERE ingredient IN (%s)"%format_strings,tuple(checkbox_ing))
        results = cursor.fetchall()
        for row in results:
                recipe_id_list = decode(row[0])
                #print(recipe_id_list)
                for recipe_id in recipe_id_list:
                    if recipe_id not in recipe_common_ing_count:
                        continue
                    else:
                        recipe_common_ing_count[recipe_id] -=1

                        #if int(recipe_id) == 7454:
                            #print(recipe_common_ing_count[recipe_id])

        recipe_dict = sorted(recipe_common_ing_count.items(),key=lambda k:k[1])
        recipe_dict_iter = recipe_dict
        recipe_list = []
        clash_dict = dict()
        clash_dict[0] = []
        time_dict = {}
        id_sql_list = []
        count_id_dict = {}
        for id, count in recipe_dict_iter:
            if count not in clash_dict:
                clash_dict[int(count)] = []
            id_sql_list.append(id)
            count_id_dict[id] = int(count)
        format_strings = ','.join(['%s'] * len(id_sql_list))
        #sql = ("""SELECT preparation_time,cook_time FROM recipe_info WHERE recipe_id LIKE %s""",id)
        cursor.execute("SELECT recipe_id,preparation_time,cook_time FROM recipe_info WHERE recipe_id IN (%s)"%format_strings,tuple(id_sql_list))
        results = cursor.fetchall()
        for row in results:
            id = row[0]
            time = int(row[1])+int(row[2])
            if (shopping_param == False and very_hungry_param == False) or (shopping_param == False and very_hungry_param == True):
                clash_dict[count_id_dict[id]].append([id,time])
            elif shopping_param == True and very_hungry_param == True:
                time_dict[id]= time
        json_dict = {'id':[],'length':"",'error':"",'message':""}
        length = 0
        """if shopping_param == False and very_hungry_param == False:
            for key,value in clash_dict.items():
                sorted_items = sorted(value,key=lambda k:k[1])
            clash_dict[key] = sorted_items
            clash_dict = sorted(clash_dict)
            for count,value in clash_dict:
                length+=len(value)
                for item in value:
                    json_dict['id'].append(item[0])
            json_dict['length'] = length
            json_dict['results_status'] = True"""
        if shopping_param == True and very_hungry_param == True:
            time_dict = sorted(time_dict.items(),key=lambda k:k[1])
            for key,value in time_dict:
                json_dict['id'].append(key)
            json_dict['length'] = len(time_dict)
            json_dict['error'] = 0
        elif (shopping_param == False and very_hungry_param == True) or (shopping_param == False and very_hungry_param == False):
            if len(clash_dict[0]) == 0:
                json_dict['error'] = 2
                for key,value in clash_dict.items():
                    sorted_items = sorted(value,key=lambda k:k[1])
                    clash_dict[key] = sorted_items
                clash_dict = sorted(clash_dict.items())
                json_dict['message'] = "Sorry! we couldn't find any results with the ingredients you have. Here are some suggestions where you might have to go to shopping"
            else:
                json_dict['error'] = 0
                clash_dict = [(0,sorted(clash_dict[0],key=lambda k:k[1]))]
            for count,value in clash_dict:
                length+=len(value)
                for item in value:
                    json_dict['id'].append(item[0])
            json_dict['length'] = length
        elif shopping_param == True and very_hungry_param == False:
            for id,count in recipe_dict_iter:
                json_dict['id'].append(id)
            json_dict['length'] = len(recipe_dict_iter)
            json_dict['error'] = 0
        if error==3:
            json_dict['error'] = error
            json_dict['message'] = "Sorry! We coudnt find any recipes for the combination of your ingredients. But here are some suggestions from our side"
        #print('success 1')
        #print(json_dict)
        return json.dumps(json_dict)



import mimetypes, urllib
def is_url_image(url):
    mimetype,encoding = mimetypes.guess_type(url)
    return (mimetype and mimetype.startswith('image'))

def check_url(url):
    """Returns True if the url returns a response code between 200-300,
       otherwise return False.
    """
    try:
        headers = {
            "Range": "bytes=0-10",
            "User-Agent": "MyTestAgent",
            "Accept": "*/*"
        }

        req = urllib.Request(url, headers=headers)
        response = urllib.urlopen(req)
        return response.code in range(200, 209)
    except Exception:
        return False

def is_image_and_ready(url):
    return is_url_image(url) and check_url(url)


images_counter = 0
title_counter = 0
@app.route("/retrieve")
def retrieve():
    import random
    random_images = ['https://images.pexels.com/photos/3338539/pexels-photo-3338539.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940',
                     'https://images.pexels.com/photos/3298607/pexels-photo-3298607.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940',
                     'https://images.pexels.com/photos/691114/pexels-photo-691114.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940',
                     'https://images.pexels.com/photos/1109197/pexels-photo-1109197.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940',
                     'https://images.pexels.com/photos/3298637/pexels-photo-3298637.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940',
                     'https://images.pexels.com/photos/3800512/pexels-photo-3800512.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940',
                     'https://images.pexels.com/photos/175753/pexels-photo-175753.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940',
                     'https://images.pexels.com/photos/3560586/pexels-photo-3560586.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940',
                     'https://images.pexels.com/photos/3298692/pexels-photo-3298692.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940',
                     'https://images.pexels.com/photos/2403392/pexels-photo-2403392.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940']
    random_titles = ['Everyday favourite!','Fine Dine!','Simple and Delicious','Make-Ahead Meal','Instant Pot Dish']
    random_desc = ['An Everlasting Meal',
                    'Fun and Delicious Stuffed Dishes',
                    'Great Food Fast',
                    'The Taste of Country Cooking',
                    'Pursuit of Flavor',
                    'Homemade no Time',
                    'Fast and Easy',
                    'Slow and Delicious',
                    'Master the Art of Cooking ',
                    'Fine Produce On The Table',
                    'Fantastic Meal',
                    'Small Recipe with a Big Flavor']
    args = request.args
    #print(args)
    recipe_ids = args['recipe_list'].strip().split(',')
    db = pymysql.connect("ttsheng.mysql.pythonanywhere-services.com","ttsheng","bft8299py","ttsheng$recipes" )
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    json_dict = dict()
    json_dict['recipe_info'] = []
    format_strings = ','.join(['%s'] * len(recipe_ids))
    #sql = ("""SELECT image_url,description, recipe_url, title FROM recipe_info WHERE recipe_id LIKE %s""",id)
    cursor.execute("SELECT image_url,description, recipe_url, title,recipe_id FROM recipe_info WHERE recipe_id IN (%s)" % format_strings,tuple(recipe_ids))
    results = cursor.fetchall()
    for row in results:
        image_url = str(row[0]).strip()
        desc = str(row[1]).strip()
        recipe_url = str(row[2]).strip()
        title = str(row[3]).strip()
        id = row[4]
        if desc.lower() == "none":
             description = random_desc[random.randint(0,len(random_desc)-1)]
             if 'Master' in description:
                 desc = description+title
             else:
                 desc = description
        if image_url.lower()=="none":
            image_url = random_images[random.randint(0,len(random_images)-1)]
        if title.lower() == "none":
            title = random_titles[random.randint(0,len(random_titles)-1)]
        #print(image_url,desc,recipe_url,title)
        json_dict['recipe_info'].append({'id':id,'src':image_url,'desc':desc,'title':title,'url':recipe_url})
    db.close()
    #print('success 2')
    #print(json_dict)
    return json.dumps(json_dict)
    #sq11 = ("""SELECT documents FROM ranking_pagerank WHERE word LIKE %s""", "%"+word+"%")
    """cursor.execute(*sq11)
    score = cursor.fetchone()
    v = float(v) * float(score[0])
    if k in docu_dict:
        if docu_dict[k] < v:
            docu_dict[k] = v
    else:
        docu_dict[k] = v

    total = time.time()-start
    docu_dict = sorted(docu_dict.items(),key=lambda x:x[1],reverse=True)


for k,v in docu_dict:
    print(k)
print(total)
"""
if __name__ == "__main__":
    app.run(debug=False,threaded=True)