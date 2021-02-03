from urllib.request import urlopen
from link_finder import LinkFinder
from domain import *
from general import *
from robots import *
import time
from bs4 import BeautifulSoup
import urllib.robotparser

class Spider:

    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    robotcheck = ''
    queue = set()
    crawled = set()
    ingredients_count = 0
    def __init__(self, project_name, base_url, domain_name):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.robotcheck = checkrobots(domain_name)

        Spider.queue_file = Spider.project_name + '/queue.txt'
        Spider.crawled_file = Spider.project_name + '/crawled.txt'

        self.boot()
        self.crawl_page('First spider', Spider.base_url)

    # Creates directory and files for project on first run and starts the spider
    @staticmethod
    def boot():
        create_project_dir(Spider.project_name)
        existing_status = create_data_files(Spider.project_name, Spider.base_url)
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)
        return existing_status
        
    # Updates user display, fills queue and updates files
    @staticmethod
    def crawl_page(thread_name, page_url):
        #print(Spider.robotcheck.can_fetch("*",page_url))
        if Spider.robotcheck.can_fetch("*",page_url):
            page_url = page_url.strip().split(" ")
            #print(len(page_url))
            if len(page_url) == 1:
                delay = Spider.robotcheck.crawl_delay("*")
                if delay is None:
                    delayed_time = time.time()
                else:
                    delayed_time = Spider.robotcheck.crawl_delay("*")+time.time()
                #print(Spider.queue)
                #print(page_url[0])
                try:
                    Spider.queue.remove(page_url[0])
                    #print(Spider.queue)
                    Spider.queue.add(page_url[0]+" "+str(delayed_time))
                    #print(Spider.queue)
                    Spider.update_files()
                except:
                    pass
            elif len(page_url) == 2:
                wait_time = float(page_url[-1])
                if time.time() >= wait_time:
                    if page_url[0] not in Spider.crawled:
                        print(thread_name + ' now crawling ' + page_url[0])
                        print('Queue ' + str(len(Spider.queue)) + ' | Crawled  ' + str(len(Spider.crawled)))
                        Spider.add_links_to_queue(Spider.gather_links(page_url[0]))
                    try:
                        Spider.queue.remove(page_url[0]+" "+str(wait_time))
                        Spider.crawled.add(page_url[0])
                        Spider.update_files()
                    except:
                        pass
    # Converts raw response data into readable information and checks for proper html formatting
    @staticmethod
    def gather_links(page_url):
        html_string = ''
        try:
            response = urlopen(page_url)
            if 'text/html' in response.getheader('Content-Type'):
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
            finder = LinkFinder(Spider.base_url, page_url)
            finder.feed(html_string)
            soup = BeautifulSoup(html_string, 'html.parser')
            if page_url.__contains__("www.bbc.co.uk/food/recipes/"):

                with open((Spider.project_name+'/content.txt'),'a',encoding='UTF-8') as f:
                    recipie_url = page_url
                    recipie_title = soup.find("h1",{"class" :"gel-trafalgar content-title__text"}).text
                    f.write(recipie_url+"\n")
                    try:
                        recipie_imageurl = soup.find("div",{"class":"responsive-image-container__16/9"}).find('img').get('src')
                    except:
                        recipie_imageurl = "None"
                    f.write(recipie_imageurl+"\n")
                    f.write(recipie_title+"\n")
                    #print(recipie_rating)
                    #recipie_norating = soup.find("span",{"class" :"aggregate-rating__total gel-long-primer-bold"}).text
                    #print(recipie_norating)
                    try:
                        recipie_content = soup.find("p",{'class':'recipe-description__text'}).text
                    except:
                        recipie_content = "None"
                    f.write(recipie_content+"\n"+"preptime:-\n")
                    try:
                        recipie_prep = soup.find("p",{'class':'recipe-metadata__prep-time'}).text
                    except:
                        recipie_prep = "None"
                    f.write(recipie_prep+"\n")
                    try:
                        recipie_cook = soup.find("p",{'class':'recipe-metadata__cook-time'}).text
                    except:
                        recipie_cook = "None"
                    f.write(recipie_cook+"\n")
                    try:
                        recipie_serves = soup.find("p",{'class':'recipe-metadata__serving'}).text
                    except:
                        recipie_serves = "None"
                    f.write(recipie_serves+"\n")
                    try:
                        ingre_list = soup.find_all("ul",{'class':'recipe-ingredients__list'})
                        ingredients = ""
                        for rows in ingre_list:
                            for row in rows:
                                ingredients += (row.text+"\n")
                    except:
                        ingredients = "None"
                    f.write(ingredients)
                    eol = "*****eol*****"
                    f.write(eol+"\n")
                    #f.write(recipie_url+"\n"+recipie_imageurl+"\n"+recipie_title+"\n"+recipie_content+"\npreptime:-\n"+recipie_prep+"\n"+recipie_cook+"\n"+recipie_serves+"\n"+ingredients+eol+"\n")
                    Spider.ingredients_count += 1
                    print(Spider.ingredients_count)



            """title = soup.title.string
            for script in soup(["script", "style","head","meta",'[document]',"header","noscript","footer","div.ng-scope"]):
                script.extract()
            text = soup.get_text()
            # break into lines and remove leading and trailing space on eac
            lines = (line.strip() for line in text.splitlines())
            # break multi-headlines into a line each
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            # drop blank lines
            text = '\n'.join(chunk for chunk in chunks if chunk)

            file_name= Spider.project_name + '/contents.txt'
            with open(file_name,"a",encoding="UTF-8") as f:
                f.write(page_url + " " + title+ " " + text + "\n")
                f.write("*****eol*****\n")"""
        except Exception as e:
            print(str(e))
            return set()
        return finder.page_links()

    # Saves queue data to project files
    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            url = url.strip().split(" ")[0]
            if (url in Spider.queue) or (url in Spider.crawled):
                continue

            if Spider.domain_name != get_domain_name(url):
                continue
            if "www.bbc.co.uk/food/" not in url or "/shopping-list" in url:
                continue
            Spider.queue.add(url)

    @staticmethod
    def update_files():
        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)
