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
import googlemaps
from django.conf import settings
from django.contrib.auth.views import PasswordResetView
from django.shortcuts import render
from django.shortcuts import render
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
import markdown
from django.shortcuts import render
from info.helpers.newsapi_helper import NewsAPIHelper
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.views.decorators.csrf import csrf_protect

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
    google_maps_client = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)  # API key from settings
    if request.method == 'POST':
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

        # Save the generated itinerary to the session
        itinerary = response.get('text', '')
        request.session['itinerary'] = itinerary

        if 'download' in request.POST:
            days = request.POST.get('days')
            itinerary = request.session.get('itinerary', 'No itinerary available.')  # Retrieve saved itinerary
            return generate_pdf_itinerary(itinerary, city_name)
        # Get top dining spots and landmarks using Google Maps API
        dining_info = google_maps_client.places(query="restaurants in " + city_name)
        landmark_info = google_maps_client.places(query="landmarks in " + city_name)
        
        return render(request, 'info/itinerary.html', {
            'city': city_name,
            'itinerary': itinerary,
            'dining_info': dining_info['results'],
            'landmark_info': landmark_info['results'],
        })
    
    return render(request, 'info/itinerary.html', {'city': city_name})

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