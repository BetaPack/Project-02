from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render
from django.contrib.auth.views import PasswordResetView
from django.shortcuts import render
from django.shortcuts import render
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
import markdown
import googlemaps
from django.conf import settings

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

def city_info(request, city_name):
    itinerary = None
    google_maps_client = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)  # API key from settings

    if request.method == 'POST':
        days = request.POST.get('days')

        # Initialize Gemini LLM
        my_llm = initialize_gemini_llm()
        my_prompt = PromptTemplate.from_template('Create an itinerary for {placename} for {num} days')
        chain = LLMChain(llm=my_llm, prompt=my_prompt, verbose=False)
        inputs = {'placename': city_name, 'num': days}
        response = chain.invoke(input=inputs)

        itinerary = response.get('text', '')

        if 'download' in request.POST:
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

# Generate PDF itinerary
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

    p.showPage()
    p.save()
    
    return response
