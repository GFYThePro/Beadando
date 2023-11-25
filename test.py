#!/usr/bin/env python3
import requests
from urllib3.exceptions import InsecureRequestWarning


token="Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6InE5Q2NoSVJfSUZ3MnJNNG54OGYtNUg4dzd4aWkyd3hiUnhFa3Nhekw3UW8ifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImluZ3Jlc3MtZXhwb3Nlci1zZWNyZXQiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiaW5ncmVzcy1leHBvc2VyIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQudWlkIjoiYzNhYzg1N2QtODFmYy00MzRlLWIzNGUtMzNmYzUxNGQ5MzQwIiwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50OmRlZmF1bHQ6aW5ncmVzcy1leHBvc2VyIn0.CUh92Dp-oVj4qnlIeZ4Uxn548J_DnaBa4iDGEV16hwPwaYvnqbLtyPdctCB7ndo31CzSiojokMvC_r7RJ89EbSaCs2We_W0vrSYo2jLbcbl0pYwNTZctOyBnKo713dQANI7ooHGUMqXlIez8c66yRbtj6io9AzISS1UGE2LeN-z-vgkayghbH69QzoReuWFfdI7lLcrNzopqyPJElPqT8f8i2-NYFOOKL8STFoO7PVoV-LR33iwKXIE4ki_bkW283wFLoJ8bPGTzUkxIaiKOyRrNUuLCyr6Es8prENAZFiQvITvaPjaiDifaP08D9PHyZOlK43Fc1ZG8Xv8UAheIbA"
base_url="https://192.168.253.10:6443"

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


if __name__ == "__main__":
    ns_url=base_url+"/api/v1/namespaces"
    req_ns = requests.get(ns_url, 
        headers={"Authorization":token}
        ,verify=False)
    ns_resp_json=req_ns.json()
    namespaces=[]
    print("Namespaces:")
    for item in ns_resp_json["items"]:
        namespaces.append(item["metadata"]["name"])
        print("\t-:"+item["metadata"]["name"])
    
    print("ingresses:")
    for ns in namespaces:
        print("\t-:"+ns+":")
        ing_url=base_url+"/apis/networking.k8s.io/v1/namespaces/"+ns+"/ingresses"
        req_ing = requests.get(ing_url, 
        headers={"Authorization":token}
        ,verify=False)
        ing_res_json=req_ing.json()
        for item in ing_res_json["items"]:
            for rule in item["spec"]["rules"]:
                for path in rule["http"]["paths"]:
                    print("\t\t-:"+rule["host"]+path["path"])
