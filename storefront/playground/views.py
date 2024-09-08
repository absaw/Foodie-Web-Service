from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
import requests
import json
import googlemaps
import os
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

def get_home(request):
    if request.method == "GET":
        return render(request, 'home.html')

    elif request.method == "POST":
        address = request.POST.get('address')
        
        try:
            # Load API keys
            key_path = os.path.join(settings.BASE_DIR, 'keys.json')
            with open(key_path, 'r') as key_file:
                key_dict = json.load(key_file)
        except FileNotFoundError:
            return JsonResponse({'error': 'API key file not found'}, status=500)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid API key file'}, status=500)

        # Google Maps Geocoding
        try:
            gmaps = googlemaps.Client(key=key_dict['GMAP_GEOCODING_API_KEY'])
            g_response = gmaps.geocode(address)
        except googlemaps.exceptions.ApiError as e:
            return JsonResponse({'error': f'Google Maps API error: {str(e)}'}, status=500)
        except KeyError:
            return JsonResponse({'error': 'Google Maps API key not found'}, status=500)

        if not g_response:
            return JsonResponse({'error': 'Unable to geocode the address'}, status=400)

        g_result = g_response[0]
        latitude = g_result['geometry']['location']['lat']
        longitude = g_result['geometry']['location']['lng']

        # Yelp API request
        yelp_url = f"https://api.yelp.com/v3/businesses/search"
        try:
            headers = {
                "Authorization": f"Bearer {key_dict['YELP_API_KEY']}",
            }
        except KeyError:
            return JsonResponse({'error': 'Yelp API key not found'}, status=500)

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "sort_by": "best_match",
            "limit": 5,
            "categories": "restaurants",
            "open_now":True,
            # "radius":20000,
            
        }

        try:
            yelp_response = requests.get(yelp_url, headers=headers, params=params)
            yelp_response.raise_for_status()
            restaurants = yelp_response.json()['businesses']
        except requests.RequestException as e:
            return JsonResponse({'error': f'Yelp API error: {str(e)}'}, status=500)
        except KeyError:
            return JsonResponse({'error': 'Unexpected response from Yelp API'}, status=500)

        context = {
            'address': address,
            'geo_coordinates': [latitude, longitude],
            'restaurants': restaurants
        }

        return render(request, 'home.html', context)