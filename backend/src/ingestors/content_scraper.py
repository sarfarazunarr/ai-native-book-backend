from typing import Dict, List
import httpx
import asyncio
from bs4 import BeautifulSoup
import logging


logger = logging.getLogger(__name__)


class ContentScraper:
    """Class to scrape content from URLs using async HTTP requests."""
    
    def __init__(self, max_concurrent_requests: int = 10, timeout: float = 10.0):
        """
        Initialize the content scraper.
        
        Args:
            max_concurrent_requests: Maximum number of concurrent requests
            timeout: Request timeout in seconds
        """
        self.max_concurrent_requests = max_concurrent_requests
        self.timeout = timeout
        self.semaphore = asyncio.Semaphore(max_concurrent_requests)
    
    async def scrape_urls(self, urls: List[str]) -> List[Dict[str, str]]:
        """
        Scrape content from a list of URLs concurrently.
        
        Args:
            urls: List of URLs to scrape
            
        Returns:
            List of dictionaries with 'url', 'title', and 'content' keys
        """
        tasks = [self._scrape_single_url(url) for url in urls]
        
        # Execute all scraping tasks concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out any errors and log them
        successful_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Error scraping {urls[i]}: {str(result)}")
            else:
                successful_results.append(result)
        
        logger.info(f"Successfully scraped {len(successful_results)} out of {len(urls)} URLs")
        return successful_results
    
    async def _scrape_single_url(self, url: str) -> Dict[str, str]:
        """
        Scrape content from a single URL.
        
        Args:
            url: URL to scrape
            
        Returns:
            Dictionary with 'url', 'title', and 'content' keys
        """
        async with self.semaphore:  # Limit concurrent requests
            try:
                logger.debug(f"Scraping {url}")
                
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.get(url)
                    
                    if response.status_code != 200:
                        raise Exception(f"HTTP {response.status_code} when scraping {url}")
                    
                    # Parse the HTML content
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Extract title
                    title_tag = soup.find('title')
                    title = title_tag.get_text().strip() if title_tag else 'No Title'
                    
                    # Extract content (we'll return the full text for cleaning later)
                    content = soup.get_text(separator=' ')
                    
                    result = {
                        'url': url,
                        'title': title,
                        'content': content
                    }
                    
                    logger.debug(f"Successfully scraped {url}")
                    return result
                    
            except Exception as e:
                logger.error(f"Error scraping {url}: {str(e)}")
                raise