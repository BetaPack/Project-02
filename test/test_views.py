import pytest
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

@pytest.mark.django_db
def test_news_page_loads(client):
    """Test if the news page for a city loads successfully."""
    response = client.get(reverse("info:city_news", args=["new-york", "usa"]))
    assert response.status_code == 200
    assert "Latest News in New York" in response.content.decode()

@pytest.mark.django_db
def test_news_articles_display(client):
    """Test if news articles are displayed on the news page."""
    # Mock data for news articles to simulate the context
    news_articles = [
        {
            "title": "Example News 1",
            "url": "https://example.com/news1",
            "source": {"name": "Example Source 1"},
            "publishedAt": timezone.now() - timedelta(days=1),
            "description": "Description of example news 1.",
        },
        {
            "title": "Example News 2",
            "url": "https://example.com/news2",
            "source": {"name": "Example Source 2"},
            "publishedAt": timezone.now() - timedelta(days=2),
            "description": "Description of example news 2.",
        },
    ]
    # Mock the view to render the template with mock data
    response = client.get(reverse("info:city_news", args=["new-york", "usa"]), {"news_articles": news_articles, "city": "New York"})
    assert response.status_code == 200
    content = response.content.decode()

    # Check if article titles and descriptions appear on the page
    for article in news_articles:
        assert article["title"] in content
        assert article["description"] in content
        assert article["source"]["name"] in content

@pytest.mark.django_db
def test_no_news_message(client):
    """Test if the 'No news available' message is displayed when there are no articles."""
    response = client.get(reverse("info:city_news", args=["new-york", "usa"]))
    content = response.content.decode()

    # Check if the 'No news available' message appears
    assert "No news available for this location." in content

@pytest.mark.django_db
def test_news_links_open_in_new_tab(client):
    """Test if news article links open in a new tab."""
    news_articles = [
        {
            "title": "Example News 1",
            "url": "https://example.com/news1",
            "source": {"name": "Example Source 1"},
            "publishedAt": timezone.now() - timedelta(days=1),
            "description": "Description of example news 1.",
        }
    ]
    response = client.get(reverse("info:city_news", args=["new-york", "usa"]), {"news_articles": news_articles, "city": "New York"})
    content = response.content.decode()

    # Check if the link has the target="_blank" attribute to open in a new tab
    assert 'href="https://example.com/news1"' in content
    assert 'target="_blank"' in content
