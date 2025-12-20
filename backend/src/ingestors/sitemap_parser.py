from typing import List
import httpx
import xml.etree.ElementTree as ET
from urllib.parse import urlparse
import logging


logger = logging.getLogger(__name__)


class SitemapParser:
    """Class to parse sitemaps and extract URLs."""
    
    def __init__(self, base_domain: str = None):
        """
        Initialize the sitemap parser.
        
        Args:
            base_domain: Optional domain to filter URLs by
        """
        self.base_domain = base_domain
    
    def parse_sitemap_content(self, sitemap_content: str) -> List[str]:
        """
        Parse sitemap XML content and extract URLs.
        
        Args:
            sitemap_content: XML content of the sitemap
            
        Returns:
            List of extracted URLs
        """
        try:
            # Parse the XML content
            root = ET.fromstring(sitemap_content)
            
            # Handle both regular sitemap and sitemap index
            urls = []
            
            # Define namespaces for XML parsing
            namespaces = {
                'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9',
                'index': 'http://www.sitemaps.org/schemas/sitemap/0.9'
            }
            
            # Extract URLs from url elements
            for url_element in root.findall('sitemap:url', namespaces):
                loc_element = url_element.find('sitemap:loc', namespaces)
                if loc_element is not None:
                    url = loc_element.text.strip()
                    
                    # Filter by base domain if specified
                    if self.base_domain:
                        parsed_url = urlparse(url)
                        if parsed_url.netloc != self.base_domain:
                            continue
                    
                    urls.append(url)
            
            logger.info(f"Parsed {len(urls)} URLs from sitemap")
            return urls
            
        except ET.ParseError as e:
            logger.error(f"Error parsing sitemap XML: {str(e)}")
            raise
        
        except Exception as e:
            logger.error(f"Unexpected error parsing sitemap content: {str(e)}")
            raise
    
    def parse_sitemap_from_url(self, sitemap_url: str) -> List[str]:
        """
        Download and parse a sitemap from a URL.
        
        Args:
            sitemap_url: URL of the sitemap to download and parse
            
        Returns:
            List of extracted URLs
        """
        try:
            logger.info(f"Downloading sitemap from {sitemap_url}")
            
            # Use httpx to download the sitemap
            with httpx.Client() as client:
                response = client.get(sitemap_url, timeout=30.0)
                
                if response.status_code != 200:
                    raise Exception(f"HTTP {response.status_code} when downloading sitemap")
                
                # Parse the content
                urls = self.parse_sitemap_content(response.text)
                
                logger.info(f"Downloaded and parsed sitemap from {sitemap_url}, found {len(urls)} URLs")
                return urls
                
        except httpx.RequestError as e:
            logger.error(f"Error downloading sitemap from {sitemap_url}: {str(e)}")
            raise
        
        except Exception as e:
            logger.error(f"Unexpected error parsing sitemap from URL: {str(e)}")
            raise