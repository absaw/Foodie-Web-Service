from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests
import googlemaps
from django.conf import settings

@csrf_exempt
def get_restaurants(request):
    if request.method == "GET":
        return render(request,'home.html')
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            address = data.get('address')

            if not address:
                return JsonResponse({'error': 'Address is required'}, status=400)

            # Load API keys (consider moving this to environment variables)
            key_dict = settings.API_KEYS

            # Google Maps Geocoding
            gmaps = googlemaps.Client(key=key_dict['GMAP_GEOCODING_API_KEY'])
            g_response = gmaps.geocode(address)

            if not g_response:
                return JsonResponse({'error': 'Unable to geocode the address'}, status=400)

            g_result = g_response[0]
            latitude = g_result['geometry']['location']['lat']
            longitude = g_result['geometry']['location']['lng']

            # Yelp API request
            yelp_url = "https://api.yelp.com/v3/businesses/search"
            headers = {
                "Authorization": f"Bearer {key_dict['YELP_API_KEY']}",
            }
            params = {
                "latitude": latitude,
                "longitude": longitude,
                "sort_by": "rating",
                "limit": 5,
                "categories": "restaurants"
            }

            yelp_response = requests.get(yelp_url, headers=headers, params=params)
            yelp_response.raise_for_status()
            restaurants = yelp_response.json()['businesses']

            return JsonResponse({
                'restaurants': restaurants,
                'address': address,
                'geo_coordinates': [latitude, longitude]
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)