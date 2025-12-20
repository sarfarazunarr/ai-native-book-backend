import pytest
from unittest.mock import Mock, patch, mock_open
import sys
import os
import xml.etree.ElementTree as ET

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.ingestors.sitemap_parser import SitemapParser


# Sample sitemap XML content for testing
SAMPLE_SITEMAP_XML = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
   <url>
      <loc>https://physical-ai-humanoid-robotics-omega.vercel.app/</loc>
      <lastmod>2023-10-15</lastmod>
      <changefreq>weekly</changefreq>
      <priority>1.0</priority>
   </url>
   <url>
      <loc>https://physical-ai-humanoid-robotics-omega.vercel.app/introduction</loc>
      <lastmod>2023-10-15</lastmod>
      <changefreq>weekly</changefreq>
      <priority>0.8</priority>
   </url>
   <url>
      <loc>https://physical-ai-humanoid-robotics-omega.vercel.app/actuators</loc>
      <lastmod>2023-10-15</lastmod>
      <changefreq>weekly</changefreq>
      <priority>0.7</priority>
   </url>
</urlset>"""


def test_sitemap_parser_initialization():
    """Test that the SitemapParser initializes correctly."""
    parser = SitemapParser()
    
    # Verify that the parser has the expected attributes
    assert hasattr(parser, 'base_domain_filter')
    assert parser.base_domain_filter is None


def test_parse_sitemap_content():
    """Test parsing sitemap XML content."""
    parser = SitemapParser()
    
    # Parse the sample sitemap
    urls = parser.parse_sitemap_content(SAMPLE_SITEMAP_XML)
    
    # Verify that we got the right number of URLs
    assert len(urls) == 3
    
    # Verify the content of the URLs
    expected_urls = [
        "https://physical-ai-humanoid-robotics-omega.vercel.app/",
        "https://physical-ai-humanoid-robotics-omega.vercel.app/introduction",
        "https://physical-ai-humanoid-robotics-omega.vercel.app/actuators"
    ]
    
    for i, url in enumerate(urls):
        assert url == expected_urls[i]


def test_parse_sitemap_content_with_domain_filter():
    """Test parsing sitemap with domain filtering."""
    parser = SitemapParser(base_domain="physical-ai-humanoid-robotics-omega.vercel.app")
    
    # Parse the sample sitemap with domain filtering
    urls = parser.parse_sitemap_content(SAMPLE_SITEMAP_XML)
    
    # Verify that we got the right number of URLs (should be same since all match)
    assert len(urls) == 3
    
    # Verify that all URLs belong to the correct domain
    for url in urls:
        assert "physical-ai-humanoid-robotics-omega.vercel.app" in url


def test_parse_sitemap_content_with_different_domain():
    """Test that URLs from different domains are filtered out."""
    # Sample sitemap with a URL from a different domain
    different_domain_sitemap = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
   <url>
      <loc>https://physical-ai-humanoid-robotics-omega.vercel.app/</loc>
   </url>
   <url>
      <loc>https://different-domain.com/page</loc>
   </url>
</urlset>"""
    
    parser = SitemapParser(base_domain="physical-ai-humanoid-robotics-omega.vercel.app")
    
    # Parse the sitemap with domain filtering
    urls = parser.parse_sitemap_content(different_domain_sitemap)
    
    # Should only return URLs from the specified domain
    assert len(urls) == 1
    assert urls[0] == "https://physical-ai-humanoid-robotics-omega.vercel.app/"


@patch('httpx.get')
def test_parse_sitemap_from_url_success(mock_get):
    """Test parsing sitemap from a URL successfully."""
    # Mock the HTTP response
    mock_response = Mock()
    mock_response.text = SAMPLE_SITEMAP_XML
    mock_response.status_code = 200
    mock_get.return_value = mock_response
    
    parser = SitemapParser()
    
    # Parse sitemap from URL
    urls = parser.parse_sitemap_from_url("https://physical-ai-humanoid-robotics-omega.vercel.app/sitemap.xml")
    
    # Verify HTTP call was made
    mock_get.assert_called_once()
    
    # Verify the results
    assert len(urls) == 3
    expected_urls = [
        "https://physical-ai-humanoid-robotics-omega.vercel.app/",
        "https://physical-ai-humanoid-robotics-omega.vercel.app/introduction",
        "https://physical-ai-humanoid-robotics-omega.vercel.app/actuators"
    ]
    assert urls == expected_urls


@patch('httpx.get')
def test_parse_sitemap_from_url_http_error(mock_get):
    """Test parsing sitemap from a URL that returns an HTTP error."""
    # Mock the HTTP response with error
    mock_response = Mock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response
    
    parser = SitemapParser()
    
    # Should raise an exception when the server returns an error
    with pytest.raises(Exception):
        parser.parse_sitemap_from_url("https://example.com/sitemap.xml")


@patch('httpx.get')
def test_parse_sitemap_from_url_xml_error(mock_get):
    """Test parsing sitemap from a URL with invalid XML."""
    # Mock the HTTP response with invalid XML
    mock_response = Mock()
    mock_response.text = "This is not valid XML"
    mock_response.status_code = 200
    mock_get.return_value = mock_response
    
    parser = SitemapParser()
    
    # Should raise an exception when XML is invalid
    with pytest.raises(ET.ParseError):
        parser.parse_sitemap_from_url("https://example.com/sitemap.xml")