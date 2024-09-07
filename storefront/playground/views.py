from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
# Create your views here.
import requests as req 
import json
import jsonpath 
import googlemaps

def get_home(request):
    #you receive a HTTP request as parameter when the function
    #is called. 
    if request.method == "GET":
        # template = loader.get_template('home.html')
        # return HttpResponse(template.render())
        return render(request,'home.html')

    elif request.method=="POST":
        # context = {'name':'Alice'}
        # Input is address
        # Step 1 : Google Maps API: Geocode the address
        # Step 2 : YELP: Get the list of popular restaurants
        post_dict = request.POST #the form is returned as dictionary
        print(post_dict)
        address = post_dict['address']
        context = {'message':f'You entered: {address}'}
        print("Address entered: ",address)
        #Importing keys 
        key_file=open("/Users/abhishek.sawalkar/Desktop/Codefiles/Foodie-Web-Service/storefront/keys.json",'r')
        key_read=key_file.read()
        key_dict=json.loads(key_read)
        key_file.close()
        print(key_dict.keys())
        
        #Testing google geocoding api
        print("testing Geocode ")
        G_API_KEY = key_dict['GMAP_GEOCODING_API_KEY']
        gmaps = googlemaps.Client(key=G_API_KEY)
        # g_response = gmaps.geocode('401, palm island 4, Royal palms')
        g_response = gmaps.geocode(address)
        print("G Response: ",g_response)
        if g_response:
            g_result = g_response[0]
            #Extracting latitude and longitude for given location
            latitude = g_result['geometry']['location']['lat']
            longitude = g_result['geometry']['location']['lng']
            print(latitude,longitude)
            context["geo_coordinates"] = [latitude,longitude]
        

        # url = "https://api.yelp.com/v3/businesses/search?latitude=40.495569&longitude=-74.445136&sort_by=best_match&limit=20"
        auth = "Bearer "+key_dict['YELP_API_KEY']

        headers = {
            "accept": "application/json",
            "Authorization" : auth
        }

        yelp_response = req.get(url, headers=headers)
        json_res=json.loads(yelp_response.text)
        print(type(json_res))#dictionary
        with open('nb_station.json', 'w') as outfile:
            json.dump(json_res, outfile)
        # print(json_res["results"][0]["location"])
        print(yelp_response)
        
        return render(yelp_response.text,'home.html')
        return render(request,'home.html',context)
        
        
    
       
    


