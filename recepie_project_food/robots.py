def checkrobots(url):
    import urllib.robotparser
    rp = urllib.robotparser.RobotFileParser()
    url = "http://"+url+"/robots.txt"
    rp.set_url(url)
    print(url)
    rp.read()

    return rp
    #rrate = rp.request_rate("*")
    #rrate.requests
    #rrate.seconds
    #rp.crawl_delay("*")
    #rp.can_fetch("*", "http://www.musi-cal.com/cgi-bin/search?city=San+Francisco")
    #rp.can_fetch("*", "http://www.musi-cal.com/")
