from bs4 import BeautifulSoup
import re
import logging
from typing import Dict, List


logger = logging.getLogger(__name__)


class ContentCleaner:
    """Class to clean and process scraped content, removing Docusaurus boilerplate."""
    
    def __init__(self):
        """Initialize the content cleaner."""
        # Define patterns to remove common boilerplate elements
        self.boilerplate_selectors = [
            'nav',  # Navigation bars
            'footer',  # Footer sections
            '.nav',  # Navigation elements
            '.navbar',  # Navigation bars
            '.footer',  # Footer elements
            '.sidebar',  # Side navigation
            '.toc',  # Table of contents
            '.theme-edit-this-page',  # Edit links
            '.pagination-nav',  # Pagination
            '.theme-admonition',  # Admonition blocks
            'header'  # Header sections
        ]
    
    def clean_content(self, content_data: Dict[str, str]) -> Dict[str, str]:
        """
        Clean a single content entry by removing boilerplate and formatting text.
        
        Args:
            content_data: Dictionary with 'url', 'title', and 'content' keys
            
        Returns:
            Dictionary with cleaned content
        """
        try:
            # Parse the HTML to remove boilerplate elements
            soup = BeautifulSoup(content_data['content'], 'html.parser')
            
            # Remove boilerplate elements
            for selector in self.boilerplate_selectors:
                elements = soup.select(selector)
                for element in elements:
                    element.decompose()  # Remove the element from the tree
            
            # Get the cleaned text content
            cleaned_text = soup.get_text(separator=' ')
            
            # Clean up whitespace
            cleaned_text = self._clean_whitespace(cleaned_text)
            
            # Create the result with cleaned content
            result = {
                'url': content_data['url'],
                'title': self._clean_title(content_data['title']),
                'content': cleaned_text
            }
            
            logger.debug(f"Cleaned content for {content_data['url']}")
            return result
            
        except Exception as e:
            logger.error(f"Error cleaning content for {content_data['url']}: {str(e)}")
            # Return the original data if cleaning fails
            return content_data
    
    def clean_content_batch(self, content_list: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Clean a batch of content entries.
        
        Args:
            content_list: List of content entries with 'url', 'title', and 'content' keys
            
        Returns:
            List of dictionaries with cleaned content
        """
        cleaned_content = []
        
        for content_data in content_list:
            cleaned_data = self.clean_content(content_data)
            cleaned_content.append(cleaned_data)
        
        logger.info(f"Cleaned {len(cleaned_content)} content entries")
        return cleaned_content
    
    def _clean_whitespace(self, text: str) -> str:
        """
        Clean up excessive whitespace in text.
        
        Args:
            text: Raw text
            
        Returns:
            Text with normalized whitespace
        """
        # Replace multiple whitespace characters with a single space
        text = re.sub(r'\s+', ' ', text)
        
        # Remove leading and trailing whitespace
        text = text.strip()
        
        return text
    
    def _clean_title(self, title: str) -> str:
        """
        Clean up the page title.
        
        Args:
            title: Raw title
            
        Returns:
            Cleaned title
        """
        # Remove extra whitespace
        title = self._clean_whitespace(title)
        
        # Remove common suffixes like " | Website" or " | Project Name"
        title = re.sub(r'\s*\|\s*.*$', '', title)
        
        return title