#!/usr/bin/env python3
from fastapi import FastAPI,Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette_prometheus import metrics, PrometheusMiddleware
import uvicorn
import argparse
import configparser
import logging
from logic import get_ns,get_links_for_ns,get_links


token="populate at start"
base_url="populate at start"


app = FastAPI()
logging.basicConfig(level=logging.DEBUG)
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/test", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})



# If no metrics SRE ain't happy.
app.add_middleware(PrometheusMiddleware)
app.add_route('/metrics', metrics)

# Add healtcheck for K8S compatibility
@app.get("/healthcheck")
async def root():
    return {"OK"}

@app.get("/ingress")
async def ingresses(request: Request):
    urls=get_links(base_url,token)
    logging.info(urls)
    return templates.TemplateResponse("urls.html", {"request": request,"urls":urls})

# Namespaces page
@app.get("/namespaces", response_class=HTMLResponse)
async def read_item(request: Request):
    namespaces=get_ns(base_url,token)
    return templates.TemplateResponse("namespace.html", {"request": request,"namespaces":namespaces})

@app.get("/links/{ns}",tags=["namespaceses"])
async def return_link_for_ns(request: Request,ns: str):
    urls=get_links_for_ns(base_url,token,ns)
    logging.info(urls)
    return templates.TemplateResponse("urls_for_ns.html", {"request": request,"urls":urls,"ns":ns})

# Main page
@app.get("/{full_path:path}", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    config = configparser.RawConfigParser()
    config.read("config.conf")
    token=config["k8s"]["token"]
    base_url=config["k8s"]["base_url"]
    uvicorn.run(app, host="0.0.0.0", port=8000)

