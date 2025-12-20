from typing import Dict, List
import logging


logger = logging.getLogger(__name__)


class ContentChunker:
    """Class to chunk content into smaller pieces for embedding."""
    
    def __init__(self, max_chunk_size: int = 500, overlap_size: int = 50):
        """
        Initialize the content chunker.
        
        Args:
            max_chunk_size: Maximum number of words per chunk
            overlap_size: Number of overlapping words between chunks
        """
        self.max_chunk_size = max_chunk_size
        self.overlap_size = overlap_size
    
    def chunk_content(self, content_data: Dict[str, str]) -> List[Dict[str, str]]:
        """
        Chunk a single content entry into smaller pieces.
        
        Args:
            content_data: Dictionary with 'url', 'title', and 'content' keys
            
        Returns:
            List of content chunks, each with 'url', 'title', and 'content' keys
        """
        try:
            content = content_data['content']
            url = content_data['url']
            title = content_data['title']
            
            # Split content into words
            words = content.split()
            
            if len(words) <= self.max_chunk_size:
                # Content is small enough, return as is
                return [content_data]
            
            chunks = []
            start_idx = 0
            
            while start_idx < len(words):
                # Determine the end index for this chunk
                end_idx = start_idx + self.max_chunk_size
                
                # Extract the chunk
                chunk_words = words[start_idx:end_idx]
                chunk_content = ' '.join(chunk_words)
                
                # Create the chunk data
                chunk_data = {
                    'url': url,
                    'title': title,
                    'content': chunk_content
                }
                
                chunks.append(chunk_data)
                
                # Move to the next chunk, accounting for overlap
                start_idx = end_idx - self.overlap_size
                
                # If the remaining content is smaller than max_chunk_size, add it as the last chunk
                if start_idx + self.max_chunk_size >= len(words):
                    if start_idx < len(words):
                        # Add the remaining content as the final chunk
                        final_chunk = ' '.join(words[start_idx:])
                        chunks.append({
                            'url': url,
                            'title': title,
                            'content': final_chunk
                        })
                    break
            
            logger.debug(f"Chunked content from {url} into {len(chunks)} pieces")
            return chunks
            
        except Exception as e:
            logger.error(f"Error chunking content for {content_data['url']}: {str(e)}")
            # Return the original content as a single chunk if chunking fails
            return [content_data]
    
    def chunk_content_batch(self, content_list: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Chunk a batch of content entries.
        
        Args:
            content_list: List of content entries with 'url', 'title', and 'content' keys
            
        Returns:
            List of content chunks, each with 'url', 'title', and 'content' keys
        """
        all_chunks = []
        
        for content_data in content_list:
            chunks = self.chunk_content(content_data)
            all_chunks.extend(chunks)
        
        logger.info(f"Chunked {len(content_list)} content entries into {len(all_chunks)} total chunks")
        return all_chunks