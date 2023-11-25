import logging
import requests
from urllib3.exceptions import InsecureRequestWarning

# I like my logs without https warnings
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


def requester(url,token):
    logging.info("\t"+url)
    try:
        req = requests.get(url, 
            headers={"Authorization":token}
            ,verify=False)
        if req.status_code !=200:
            logging.error("Token is not right")        
            exit(-1)
        return req.json()
    except:
        logging.info(url)
        logging.error("couldn't access cluster")
        exit(-1)

def get_ns(base_url,token):
    ns_resp_json=requester(base_url+"/api/v1/namespaces",token)
    namespaces=[]
    for item in ns_resp_json["items"]:
        namespaces.append(item["metadata"]["name"])
    logging.info(namespaces)
    return(namespaces)

def get_links_for_ns(base_url,token,ns):
    url=base_url+"/apis/networking.k8s.io/v1/namespaces/"+ns+"/ingresses"
    links=[]
    ing_res_json=requester(url,token)
    for item in ing_res_json["items"]:
        for rule in item["spec"]["rules"]:
            for path in rule["http"]["paths"]:
                links.append("https://"+rule["host"]+path["path"])
    return links

def get_links(base_url,token):
    url=base_url+"/apis/networking.k8s.io/v1/ingresses"
    links=[]
    ing_res_json=requester(url,token)
    for item in ing_res_json["items"]:
        for rule in item["spec"]["rules"]:
            for path in rule["http"]["paths"]:
                links.append("https://"+rule["host"]+path["path"])
    return links