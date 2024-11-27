# from django.contrib.auth.forms import UserCreationForm
# from django.urls import reverse_lazy
# from django.views import generic
 
 
# class SignUpView(generic.CreateView):
#     form_class = UserCreationForm
#     success_url = reverse_lazy("login")
#     template_name = "registration/signup.html"

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.views import PasswordResetView
from django.shortcuts import render
from django.shortcuts import render
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
import markdown
from django.shortcuts import render
import requests
from info.helpers.newsapi_helper import NewsAPIHelper
from search.helpers.photo import UnplashCityPhotoHelper
from django.core.cache import cache
from django.utils.text import slugify


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

class CustomPasswordResetView(PasswordResetView):
    def form_valid(self, form):
        print("Attempting to send password reset email...")
        return super().form_valid(form)
    
# Initialize the LLM with the Gemini API key
def initialize_gemini_llm():
    api_key = 'AIzaSyCQuxhdViKd_-H1CQxEpFsgsHEolKLEN7w' # Fetch the key from an environment variable
    if not api_key:
        raise Exception("Gemini API Key not set. Please configure the key.")
    
    # Set up the Gemini LLM
    my_llm = ChatGoogleGenerativeAI(model='gemini-pro', api_key=api_key)
    return my_llm

@csrf_protect
def city_info(request, city_name):
    itinerary = None  # To store the generated itinerary
    if request.method == 'POST':
        # Check if the "Download" button was clicked
        if 'download' in request.POST:
            days = request.POST.get('days')
            itinerary = request.session.get('itinerary', 'No itinerary available.')  # Retrieve saved itinerary
            return generate_pdf_itinerary(itinerary, city_name)

        # Get the number of days from the form input
        days = request.POST.get('days')

        # Initialize Gemini LLM
        my_llm = initialize_gemini_llm()

        # Create a prompt template with placeholders for the city and number of days
        my_prompt = PromptTemplate.from_template('Create an itinerary for {placename} for {num} days')
        
        # Create the chain
        chain = LLMChain(llm=my_llm, prompt=my_prompt, verbose=False)
        
        # Define both place and num
        inputs = {'placename': city_name, 'num': days}
        
        # Invoke the chain with both inputs
        response = chain.invoke(input=inputs)
        
        # Get the response text from the LLM
        itinerary = response.get('text', '')
        
        # Save itinerary to session for later use
        request.session['itinerary'] = itinerary
        
        return render(request, 'info/itinerary.html', {
            'city': city_name,
            'itinerary': itinerary,
            'dining_info': dining_info['results'],
            'landmark_info': landmark_info['results'],
        })
    
    return render(request, 'info/itinerary.html', {'city': city_name})


# Generate PDF from itinerary
def generate_pdf_itinerary(itinerary, city_name):
    # Create a response object
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename={city_name}_itinerary.pdf'

    # Create the PDF
    p = canvas.Canvas(response, pagesize=letter)
    p.drawString(100, 750, f"Itinerary for {city_name}")
    p.drawString(100, 730, "--------------------------------------------")
    
    # Add the itinerary to the PDF
    y_position = 710
    for line in itinerary.splitlines():
        p.drawString(100, y_position, line)
        y_position -= 20
        if y_position < 50:  # Check if the page is full
            p.showPage()
            y_position = 750
    p.showPage()
    p.save()
    
    return response
    
def city_news(request, city, country):
    news_api_helper = NewsAPIHelper()
    news_articles = news_api_helper.get_city_news(city)

    context = {
        "city": city,
        "country": country,
        "news_articles": news_articles
    }
    return render(request, "info/news.html", context)

def localized_events(request, city):
    # Ticketmaster API settings
    API_URL = "https://app.ticketmaster.com/discovery/v2/events.json"
    API_KEY = "PvA6nBY89MHNAG6jrquNBGidGlkkhwkl"

    params = {
        "apikey": API_KEY,
        "city": city,
        "radius": 50,
        "unit": "miles",
        "size": 10,
        "sort": "date,asc",
    }

    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()

        raw_events = response.json().get("_embedded", {}).get("events", [])
        events = []
        for event in raw_events:
            # Extract event details
            name = event.get("name")
            url = event.get("url", "#")
            date = event.get("dates", {}).get("start", {}).get("localDate")
            time = event.get("dates", {}).get("start", {}).get("localTime", "TBA")
            venue = event.get("_embedded", {}).get("venues", [{}])[0].get("name")
            city_name = event.get("_embedded", {}).get("venues", [{}])[0].get("city", {}).get("name")
            price_min = event.get("priceRanges", [{}])[0].get("min")
            price_max = event.get("priceRanges", [{}])[0].get("max")
            image = event.get("images", [{}])[0].get("url")
            description = event.get("info", "No description available")

            # Calculate completeness score
            completeness_score = sum([
                2 if bool(description and description != "No description available") else 0,  # +2 if description exists
                bool(venue),  # +1 if venue exists
                bool(price_min and price_max),  # +1 if price range exists
                3 if bool(image) else 0,  # +3 if image exists
            ])

            # Append event with all details and score
            events.append({
                "name": name,
                "url": url,
                "date": date,
                "time": time,
                "venue": venue,
                "city": city_name,
                "price_min": price_min,
                "price_max": price_max,
                "image": image,
                "description": description,
                "score": completeness_score,  # Include score for sorting
            })

        # Sort events by score in descending order
        events.sort(key=lambda e: e["score"], reverse=True)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching events: {e}")
        events = []

    return render(request, "info/events.html", {"events": events, "city": city})

def city_recommendations(request):
    recommendation_type = request.GET.get("type")  # Get the selected recommendation type
    recommendations = None

    # Predefined city recommendations
    CITY_RECOMMENDATIONS = {
        "most_events": [
            {"name": "New York", "country": "US", "description": "The city that never sleeps, hosting countless events.", "image": "path/to/new_york.jpg"},
            {"name": "Los Angeles", "country": "US","description": "The entertainment capital of the world.", "image": "path/to/los_angeles.jpg"},
            {"name": "Chicago", "country": "US","description": "Known for its music festivals and cultural events.", "image": "path/to/chicago.jpg"},
            {"name": "Miami", "country": "US","description": "A hub for international art fairs and music festivals.", "image": "path/to/miami.jpg"},
            {"name": "Austin", "country": "US","description": "The live music capital of the world.", "image": "path/to/austin.jpg"},
            {"name": "Las Vegas", "country": "US","description": "Renowned for its vibrant nightlife and shows.", "image": "path/to/las_vegas.jpg"},
            {"name": "San Francisco", "country": "US","description": "Home to iconic events like Pride and Fleet Week.", "image": "path/to/san_francisco.jpg"},
            {"name": "Seattle", "country": "US","description": "Famous for its cultural festivals and concerts.", "image": "path/to/seattle.jpg"},
            {"name": "Boston", "country": "US","description": "Known for its historical and cultural events.", "image": "path/to/boston.jpg"},
            {"name": "Nashville", "country": "US","description": "The heart of country music and live performances.", "image": "path/to/nashville.jpg"}
        ],
        "landmarks": [
            {"name": "Paris", "country": "FR","description": "Home to the Eiffel Tower, Louvre, and Notre-Dame.", "image": "path/to/paris.jpg"},
            {"name": "Rome", "country": "IT","description": "The eternal city, rich with ancient landmarks like the Colosseum.", "image": "path/to/rome.jpg"},
            {"name": "London", "country": "GB","description": "Famous for Big Ben, the Tower Bridge, and Buckingham Palace.", "image": "path/to/london.jpg"},
            {"name": "Tokyo", "country": "JP","description": "Known for its historic temples and traditional gardens.", "image": "path/to/kyoto.jpg"},
            {"name": "Athens", "country": "GR","description": "The cradle of Western civilization with the Acropolis.", "image": "path/to/athens.jpg"},
            {"name": "Beijing", "country": "CN", "description": "Home to the Great Wall and the Forbidden City.", "image": "path/to/beijing.jpg"},
            {"name": "Istanbul", "country": "TR", "description": "A bridge between Europe and Asia with iconic landmarks.", "image": "path/to/istanbul.jpg"},
            {"name": "Machu Picchu", "country": "PE", "description": "The ancient Inca citadel high in the Andes.", "image": "path/to/machu_picchu.jpg"},
            {"name": "Cairo", "country": "EG", "description": "Famous for the Pyramids of Giza and the Sphinx.", "image": "path/to/cairo.jpg"},
            {"name": "New Delhi", "country": "IN", "description": "Known for the Red Fort, India Gate, and Qutub Minar.", "image": "path/to/new_delhi.jpg"}
        ],
        "dining": [
            {"name": "Tokyo", "country": "JP","description": "A global hub for sushi, ramen, and Michelin-starred restaurants.", "image": "path/to/tokyo.jpg"},
            {"name": "Paris", "country": "FR","description": "Known for its exquisite pastries and haute cuisine.", "image": "path/to/paris.jpg"},
            {"name": "Bangkok", "country": "TH","description": "A street food paradise offering incredible flavors.", "image": "path/to/bangkok.jpg"},
            {"name": "Barcelona", "country": "ES","description": "Famous for its tapas and Catalan cuisine.", "image": "path/to/barcelona.jpg"},
            {"name": "New York", "country": "US","description": "Diverse dining options from pizza to fine dining.", "image": "path/to/new_york.jpg"},
            {"name": "Istanbul", "country": "TR","description": "A blend of Middle Eastern and Mediterranean flavors.", "image": "path/to/istanbul.jpg"},
            {"name": "Hong Kong", "country": "CN","description": "Renowned for its dim sum and Cantonese cuisine.", "image": "path/to/hong_kong.jpg"},
            {"name": "Rome", "country": "IT","description": "Known for its authentic pasta, pizza, and gelato.", "image": "path/to/rome.jpg"},
            {"name": "Singapore", "country": "SG","description": "Home to the iconic hawker stalls and fusion cuisine.", "image": "path/to/singapore.jpg"},
            {"name": "San Francisco", "country": "US","description": "A foodie's paradise with world-class restaurants.", "image": "path/to/san_francisco.jpg"}
        ],
        "art": [
            {"name": "Florence", "country": "IT", "description": "The birthplace of the Renaissance and Michelangelo's David.", "image": "path/to/florence.jpg"},
            {"name": "Paris", "country": "FR", "description": "Home to the Louvre and Musée d'Orsay.", "image": "path/to/paris.jpg"},
            {"name": "New York", "country": "US", "description": "Renowned for MoMA and the Met.", "image": "path/to/new_york.jpg"},
            {"name": "London", "country": "GB", "description": "Famous for the British Museum and Tate Modern.", "image": "path/to/london.jpg"},
            {"name": "Berlin", "country": "DE", "description": "A modern art hub with countless galleries.", "image": "path/to/berlin.jpg"},
            {"name": "Venice", "country": "IT", "description": "Known for its Biennale art exhibitions.", "image": "path/to/venice.jpg"},
            {"name": "Amsterdam", "country": "NL", "description": "Home to the Van Gogh Museum and Rijksmuseum.", "image": "path/to/amsterdam.jpg"},
            {"name": "Vienna", "country": "AT", "description": "Rich with classical art and architecture.", "image": "path/to/vienna.jpg"},
            {"name": "Tokyo", "country": "JP", "description": "A blend of traditional and modern art.", "image": "path/to/tokyo.jpg"},
            {"name": "Los Angeles", "country": "US", "description": "Home to the Getty Center and LACMA.", "image": "path/to/los_angeles.jpg"}
        ]
    }

    recommendations = CITY_RECOMMENDATIONS.get(recommendation_type, [])

    for city in recommendations:
        city["photo_link"] = generate_city_photo_link(city["name"])

    return render(request, "info/recommendations.html", {
        "recommendations": recommendations,
        "type": recommendation_type,
    })

def generate_city_photo_link(city_name):
    # Generate a sanitized cache key
    cache_key = slugify(f"{city_name}-photo_link")
    photo_link = cache.get(cache_key)
    if not photo_link:
        photo_link = UnplashCityPhotoHelper().get_city_photo(city=city_name)
        cache.set(cache_key, photo_link, timeout=60 * 60 * 24)  # Cache for 24 hours
    return photo_link

