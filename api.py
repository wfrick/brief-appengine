import httplib, urllib, base64, json #Bing

def bing(key,term,number_of_results,offset,news=False,sites=[]):
    #Takes a search term, number of results, offset
    #News = True means a Bing news search, else web search
    #Returns list of urls
    #Documentation: https://dev.cognitive.microsoft.com/docs/services

    count = 0
    sites_string = ' ('
    if len(sites) > 0:
        while count < len(sites):
            if count == len(sites) - 1:
                site = 'site:'+str(sites[count])
                sites_string = sites_string + site
            else:
                site = 'site:'+str(sites[count])+' OR '
                sites_string = sites_string + site
            count +=1
        term = term + sites_string    

    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': key,
    }

    params = urllib.urlencode({
        # Request parameters
        'q': term,
        'count': number_of_results,
        'offset': offset,
        'mkt': 'en-us',
        'safeSearch': 'Moderate'
        #'freshness': 'Month'
    })

    try:
        conn = httplib.HTTPSConnection('api.cognitive.microsoft.com')
        if news == True:
            conn.request("GET", "/bing/v7.0/news/search?%s" % params, "{body}", headers)
        else:
            conn.request("GET", "/bing/v7.0/search?%s" % params, "{body}", headers)

        response = conn.getresponse()
        data = response.read()
        conn.close()
        results = json.loads(data)
        #Return articles
        articles = []
        count = 0

        while count < number_of_results:
            if news == True:
                url = results['value'][count]['url']
            else:
                url = results['webPages']['value'][count]['url']
            articles.append(url)
            count +=1
        return articles
    except Exception as e:
        return e
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
    


def agolo(key,num_sentences,URL):
    #Takes a key, a number of sentences, and a url. Returns Agolo summary object
    #Documentation: https://dev.agolo.com/docs/services/570d7b4f88b6e5116cdf6a17/operations/570d7b5188b6e508dcfb1c90
    
    body = {
        "summary_length": num_sentences,
        "articles": [{
            "type": "article", "url": URL}
            ]
        }

    body = json.JSONEncoder().encode(body)

    
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': key,
    }

    params = urllib.urlencode({
    })

    try:
        conn = httplib.HTTPSConnection('api.agolo.com')
        conn.request("POST", "/nlp/v0.2/summarize?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        return data
    except Exception as e:
        try:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))
            return "Error"
        except:
            print "Error"
            return "Error"