from urllib.request import urlopen
from link_finder import LinkFinder
from domain import *
from general import *
from robots import *
import time
from bs4 import BeautifulSoup
from random import randint
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
        create_data_files(Spider.project_name, Spider.base_url)
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)

    # Updates user display, fills queue and updates files
    @staticmethod
    def crawl_page(thread_name, page_url):
        #print(Spider.robotcheck.can_fetch("*",page_url)
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
                    Spider.queue.add(page_url[0]+" "+str(delayed_time))
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
            if page_url.__contains__("https://www.food.com/recipe/"):
                content = ""
                file_name= Spider.project_name + '/contents.txt'
                f = open(file_name,"a")
                recipe_url = page_url
                f.write(page_url+"\n")
                recipe_image_url = soup.find("script",{"type":"application/ld+json"})
                recipe_image_url = str(recipe_image_url)
                index_start = recipe_image_url.find("image")+8
                image = ""
                for i in recipe_image_url[index_start:]:
                    if i !="\"":
                        image += i
                    else:
                        break

                print(image)
                if not len(image):
                    #ecipe_image_url = soup.find("div",{"class":"component lazy-image lazy-image-udf lead-media padding-24-bottom ugc-photos-link aspect_3x4 rendered image-loaded"}).get('data-src')
                #finally:
                    recipe_image_url = "None"
                else:
                    recipe_image_url = image
                f.write(recipe_image_url+"\n")
                try:
                    recipe_title = soup.find("div",{"class":"recipe-title"}).find('h1').text
                except:
                #    recipe_title = soup.find("h1",{"class":"headline heading-content"}).text

                    recipe_title = "None"
                f.write(recipe_title+"\n")

                try:
                    recipe_content = soup.find("div",{"class":"dek"}).find('p').text
                except:
                    #recipe_content = soup.find("p",{"class":"margin-0-auto"}).text
                #finally:
                    recipe_content = "None"
                f.write(recipe_content+"\n")
                try:
                    prep_time = soup.find("script",{"type":"application/ld+json"})
                    prep_time = str(prep_time)
                    index_start = prep_time.find("prepTime")+13
                    prep = ""
                    for i in prep_time[index_start:]:
                        if i !="\"":
                            prep += i
                        else:
                            break

                    if not len(prep):
                        #ecipe_image_url = soup.find("div",{"class":"component lazy-image lazy-image-udf lead-media padding-24-bottom ugc-photos-link aspect_3x4 rendered image-loaded"}).get('data-src')
                    #finally:
                        prep_time = "None"
                    else:
                        prep_time = prep

                    #recipe_time = soup.find_all("div",{"class":"recipe-meta-item"})
                    #prep_time = recipe_time[0].text
                except:
                    pass
                    #prep_time = "None"
                f.write("preptime:\n"+str(prep_time)+"\n")

                try:
                    cook_time = soup.find("script",{"type":"application/ld+json"})
                    cook_time = str(cook_time)
                    index_start = cook_time.find("cookTime")+13
                    cook = ""
                    for i in cook_time[index_start:]:
                        if i !="\"":
                            cook += i
                        else:
                            break

                    if not len(cook):
                        #ecipe_image_url = soup.find("div",{"class":"component lazy-image lazy-image-udf lead-media padding-24-bottom ugc-photos-link aspect_3x4 rendered image-loaded"}).get('data-src')
                    #finally:
                        cook_time = "None"
                    else:
                        cook_time = cook

                    #cook_time = soup.find("div",{"class":"recipe-facts__details recipe-facts__time"}).find('span').text
                except:
                     pass
                #    recipe_time = soup.find_all("div",{"class":"recipe-meta-item"})
                #    cook_time = recipe_time[1].text
                #finally:
                    #cook_time = "None"
                f.write(str(cook_time)+"\n")
                try:
                    servings = soup.find("div",{"class":"recipe-facts__details recipe-facts__servings"}).find('a').text


                except:
                #    recipe_time = soup.find_all("div",{"class":"recipe-meta-item"})
                #    servings = recipe_time[3].text
                #finally:
                    servings = "None"
                f.write("Serves "+servings +"\n")
                try:
                    ingre=""
                    ingredients = soup.find("ul",{"class":"recipe-ingredients__list"}).find_all('li')
                    for ing in ingredients:
                        ingre += ing.text.strip()+"\n"




                except:
                #    ingredients = soup.find_all("span",{"class":"ingredients-item-name"})
                #    ingre = ""
                #    for item in ingredients:
                #        ingre = item.text+"\n"
                #finally:
                    ingre = "None"
                f.write(ingre)
                eol="*****eol*****"

                f.write(eol+"\n")


            """title = soup.title.string
            for script in soup(["script", "style"]):
                script.extract()

            text = soup.get_text()
            # break into lines and remove leading and trailing space on eac
            lines = (line.strip() for line in text.splitlines())
            # break multi-headlines into a line each
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            # drop blank lines
            text = '\n'.join(chunk for chunk in chunks if chunk)

            file_name= Spider.project_name + '/contents.txt'
            f = open(file_name,"a")
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
            if url=="www.food.com":
                continue
            """if "allrecipes.com/recipe/" not in url:
                continue"""
            Spider.queue.add(url)

    @staticmethod
    def update_files():
        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)
