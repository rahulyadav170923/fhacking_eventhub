import json
from flask import jsonify
import unirest
headers={"X-Mashape-Key": "UJufyI4Lj9mshuzkxbrZcqcIBUgOp1DgxfejsnqnsqaDWhwGzL","Accept": "application/json"}
token="34272aa31x1a6776666a"
import requests


def scrape_region_list():
    response = unirest.get("https://devru-book-my-show-v1.p.mashape.com/regionList.php?token=34272aa31x1a6776666a&type=CT",headers=headers)
    with open('data/region_list.json','w+') as f:
        f.write(json.dumps(response.body))

def scrape_event_list():
    arr = ["PUNE"]
    dict={}
    response = unirest.get("https://devru-book-my-show-v1.p.mashape.com/eventListOut.php?regioncode="+arr[0]+"&token=34272aa31x1a6776666a&type=CT",headers=headers)
    dict["PUNE"]=response.body
    with open('data/eventlist.json','w+') as f:
        f.write(json.dumps(dict))
def scrape_event_details():
    with open ('data/eventlist.json') as f:
        data = json.loads(f.read())
    event_codes=[]
    for i in data["PUNE"]["events"]:
        event_codes.append(i["EventCode"])
    event_details={}
    for i in event_codes:
        response = unirest.get("https://devru-book-my-show-v1.p.mashape.com/eventInfoList.php?eventcode="+i+"&token=34272aa31x1a6776666a",headers=headers)
        event_details[i]=response.body
        with open('data/event_details.json','w+') as f:
            f.write(json.dumps(event_details))
"""
def get_time_details():
    with open ('data/event_details.json') as f:
        data = json.loads(f.read())
    event_details=[]
    for key,value in data.iteritems():
    """

def make_models():
    model=[]
    m=1;
    with open ('data/event_details.json') as f:
        data1 = json.loads(f.read())
    with open ('data/date_list.json') as f:
        data2 = json.loads(f.read())
    with open ('data/time_list.json') as f:
        data3 = json.loads(f.read())
    for key,value in data1.iteritems():
        p={}
        p["event_id"]=key
        p["title"]=value["eventsDetails"]["EventTitle"]
        p["banner_url"]=value["eventsDetails"]["BannerURL"]
        p["share_url"]=value["eventsDetails"]["FShareURL"]
        p["event_synopsis"]=value["eventsDetails"]["EventSynopsis"]
        p["time"]=data3[key]["timeList"][0]["ShowTimeDisplay"]
        p["venue"]=data3[key]["timeList"][0]["VenueAddress"]
        p["venue_coords"]=geocode_(p["venue"])
        p["date"]=data2[key]["dateList"][0]["ShowDateDisplay"]
        p["id"]=m
        m=m+1
        p["event_release_date"]=value["eventsDetails"]["EventReleaseDate"]
        model.append(p)
    with open('data/model.json','w+') as f:
        f.write(json.dumps(model))

def get_date_list():
    with open ('data/event_details.json') as f:
        data = json.loads(f.read())
    date_details={}
    for key,value in data.iteritems():
        response = unirest.get("https://devru-book-my-show-v1.p.mashape.com/dateList.php?eventcode="+key+"&regioncode=PUNE&token=34272aa31x1a6776666a",headers=headers)
        date_details[key]=response.body
    with open('data/date_list.json','w+') as f:
        f.write(json.dumps(date_details))

def get_time_list():
    with open ('data/date_list.json') as f:
        data = json.loads(f.read())
    time_details={}
    for key,value in data.iteritems():
        response = unirest.get("https://devru-book-my-show-v1.p.mashape.com/timeList.php?eventcode="+key+"&regioncode=PUNE&showdatecode="+value["dateList"][0]["ShowDateCode"]+"&token=34272aa31x1a6776666a",headers=headers)
        time_details[key]=response.body
    with open('data/time_list.json','w+') as f:
        f.write(json.dumps(time_details))


def geocode_(address):
    geocoding_url = "https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=AIzaSyCJ8YcVRi3v0wbpUszPeGwF-E1O1LBVL68"%address
    r = requests.get(geocoding_url,verify=False).json()
    coords = r["results"][0]["geometry"]["location"]
    return coords

def map_info():
    with open ('data/model.json') as f:
        data = json.loads(f.read())
    map=[]
    for i in data:
        p={}
        p["vaenu_coords"]=i["venue_coords"]
        p["share_url"]=i["share_url"]
        p["venue"]=i["venue"]
        p["event_name"]=i["title"]
        map.append(p)
    map=json.dumps(map)
    with open('data/mapinfo.json','w+') as f:
        f.write(json.dumps(map))




if __name__ == "__main__":
    map_info()
