# CityByte Project 2

[![Test](https://github.com/BetaPack/CityByte/actions/workflows/django.yml/badge.svg)](https://github.com/BetaPack/CityByte/actions/workflows/django.yml)
[![codecov](https://codecov.io/gh/AshwiniR1802/CityByte-main/graph/badge.svg?token=QIBKVW0QLW)](https://codecov.io/gh/AshwiniR1802/CityByte-main)
[![code_size](https://img.shields.io/github/languages/code-size/BetaPack/Project-02)](https://github.com/BetaPack/Project-02) 
[![repo_size](https://img.shields.io/github/repo-size/BetaPack/Project-02)](https://github.com/BetaPack/Project-02)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7155519.svg)](https://doi.org/10.5281/zenodo.7155519)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub issues](https://img.shields.io/github/issues/BetaPack/Project-02.svg)](https://GitHub.com/BetaPack/Project-02/issues/)
[![GitHub issues-closed](https://img.shields.io/github/issues-closed/BetaPack/Project-02.svg)](https://GitHub.com/BetaPack/Project-02/issues?q=is%3Aissue+is%3Aclosed)
[![GitHub version](https://img.shields.io/github/v/release/BetaPack/Project-02)](https://github.com/BetaPack/Project-02/releases)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Introduction
## Introduction
Moving to a new location can be a daunting endeavor, especially when you have the entire world to choose from. Finding a new home from scratch while prioritizing certain aspects might be very challenging given the variety of nations and cities. However, with the advancement of technology, information from earlier times can now be leveraged to offer a number of vital insights about a certain location. Our project succeeds in one of those objectives. We seek to present that information in our project because there are many other elements that are taken into consideration when choosing a place to reside, such as weather, temperature, entertainment options, landmark locations, education, and many more. The project is totally created using a variety of technologies, including some of the accessible APIs that are utilized to fetch real-time data.

Although this project is still in its early phases of development, it can be expanded up even further by including multiple features that can benefit society in a variety of different ways. This article offers a critical viewpoint that users can use to comprehend the project, adopt it as open source software, and add further features before releasing it to the market. The document also serves as a starting point for the project and helps developers understand the code.

The technologies listed below were used to build the entire project, and it is advised that the group of developers who take on this project in the future retain these tools on hand:

* Python3
* Django
* Pytest
* HTML
* CSS
* JavaScript
* BootStrap

Although we have used HTML, CSS and Bootstrap for the frontend logic the user can use any technologies and combine it with backend such as Angular, React etc.

#### CityByte has undergone significant improvements and new features added from the earlier project. Below are the updates:

### New Features and Code Changes:
1. **News Toggle Feature**: 
   - Implemented a **toggle option** to expand and collapse city news, giving users a richer news experience.  
   - This allows users to expand top city news into a broader news feed view for a more in-depth experience.

2. **Localized Events Recommendations**: 
   - Added functionality to **alert users** about **upcoming events and festivals** in their selected cities.
   - This feature suggests events happening in the user's chosen city, helping them plan their visits accordingly.

3. **City Recommendations**: 
   - Developed an **intelligent recommender system** using city features to suggest **similar cities** that users might want to explore.
   - This feature recommends cities with similar cultural, environmental, or architectural features based on user preferences.

### Demo Video
For a walkthrough of the updated features, watch the demo video here:  
[![Watch the video](https://markdown-videos-api.jorgenkh.no/youtube/nC0bPAi8Ksc)](https://www.youtube.com/watch?v=nC0bPAi8Ksc)



## Quick Start

#### 1. Clone the repository:  

   `git clone https://github.com/rohitgeddam/CityByte.git`

#### 2. Setup the virtual environment:  
    
`
    python -m venv venv
`


#### 3. Activate the virtual environment:  

    On Mac/Linux:    

`
      source venv/bin/activate
`
      
    On Windows:    
    
`
      venv\Scripts\activate
`
   

#### 4. Install required modules and libraries:  

`
    pip install -r requirements.txt
`


#### 5. Create .env file at ./CityByte using the below template.
   
```
    GEODB_X_RAPID_API_KEY=""
    GEODB_X_RAPID_API_HOST=""
    AMADEUS_API_KEY=""
    AMADEUS_API_SECRET_KEY=""
    UNSPLASH_API_KEY=""
    FOURSQUARE_API_KEY=""
    WEATHER_BIT_X_RAPID_API_KEY=""
    WEATHER_BIT_X_RAPID_API_HOST=""
```
Create an account in the below websites to Fetch API keys and use them in the above template.  
* [GeoDB Cities API](https://rapidapi.com/wirefreethought/api/geodb-cities/details)
* [Weather API](https://rapidapi.com/weatherbit/api/weather)
* [Amadeus API](https://developers.amadeus.com/)
* [Unsplash API](https://unsplash.com/developers)
* [Foursquare API](https://location.foursquare.com/developer/)  

#### 6. Set-up REDIS
* Follow the instructions in [Getting Started](https://redis.io/docs/getting-started/) to Install Redis in your local environment.
* Start the Redis Server: Open a terminal and run the following command:
```
   redis-server
```
* Open another terminal to start the REDIS CLI:
```
   redis-cli
```

Now, you can run the application.
#### 7. Run the application:  
   
   ``` 
   python manage.py migrate
   python manage.py runserver
   ```
  
## After adding another field to Model
Django's way of propagating changes you make to your models (adding a field, deleting a model, etc.) into your database schema.

   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

## Automatic tools - GitHub Actions
 
We use GitHub actions to automate tasks of linting, code coverage, build, tests, and security checks. The codes that perform these actions are stored as `.yml` files in the `.github/workflows` directory. The GitHub actions are triggered whenever something is pushed (or pulled) into the remote repository. The results of these automated tasks are shown as badges at the top of this README.md file. 

### Unit tests:

Unit test are performed everytime there is a push or pull into the repository. They are present in `/search/tests.py`. 

### Code Coverage: 

Code Coverage is an important metric that allows us to understand how much of the codebase is tested. `django.yml` performs this task. For more information about Code Coverage, please visit this [link](https://www.atlassian.com/continuous-delivery/software-testing/code-coverage). 

### Flake8 - Code Linting:

We are using Flake8 for linting and syntax checking, and it is performed by `Linting.yml`. For more information about Flake8, please visit this [link](https://medium.com/python-pandemonium/what-is-flake8-and-why-we-should-use-it-b89bd78073f2).
Use flake8 before you push code to GitHub. </br>
Config file present in `.flake8`.

```
flake8 <directory>
```

### Black - Code Formatter

We are using the Black code formatter to format our code before pushing it to GitHub. For more information about Black, please visit this [link](https://black.readthedocs.io/en/stable/).
Config file in `pyproject.toml`.

Run the line below everytime you push to GitHub.</br>
```
black --line-length 120 <filename>
```

If you prefer using Black in VSCode, you can add the below settings in your vscode settings:

```
{
    "python.formatting.provider": "black",
    "python.formatting.blackArgs": ["--line-length", "120"],
    "python.linting.enabled": true
}
```
  
### Pre Commit Hooks for Black Code formatting and Flake8 Linting
* run  `pre-commit install`
* Now everytime you commit, Black and Flake8 will run automatically and will not allow you to push if the code standards are not met.
<img width="694" alt="Screenshot 2022-10-07 at 11 35 40 AM" src="https://user-images.githubusercontent.com/48797475/194592802-e7d7c951-9694-4260-b537-fc017a5fd06c.png">

<sub>Image from [Ji Miranda](https://ljvmiranda921.github.io/assets/png/tuts/precommit_pipeline.png).<sub>

## License
Distributed under the MIT License. See `LICENSE` for more information

## Team Members
1. Aditya Singh: asingh78@ncsu.edu
2. Monish Erode Sridhar - merodes@ncsu.edu
3. Bahare Riahai - briahi@ncsu.edu


## Support
Concerns with the software? Please get in touch with us via one of the methods below. We are delighted to address any queries you may have about the program.

Please contact us if you experience any problems with the program, such as problems with joining up, logging in, or any other functions.
