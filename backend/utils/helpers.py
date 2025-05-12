import os
import re
import hashlib
import logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)

def get_file_extension(filename: str) -> str:
    """
    Get the file extension from a filename
    
    Args:
        filename: The filename to extract extension from
        
    Returns:
        The file extension in lowercase (without the dot)
    """
    _, ext = os.path.splitext(filename)
    return ext.lower().lstrip('.')

def get_file_hash(file_path: str) -> str:
    """
    Generate an MD5 hash of a file
    
    Args:
        file_path: Path to the file
        
    Returns:
        The MD5 hash of the file
    """
    hash_md5 = hashlib.md5()
    
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception as e:
        logger.error(f"Failed to generate file hash: {str(e)}")
        return ""

def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename by removing invalid characters
    
    Args:
        filename: The filename to sanitize
        
    Returns:
        A sanitized filename
    """
    # Replace invalid characters with underscores
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Ensure the filename is not too long
    max_length = 255
    if len(sanitized) > max_length:
        base, ext = os.path.splitext(sanitized)
        sanitized = base[:max_length - len(ext)] + ext
        
    return sanitized

def extract_text_metadata(text: str) -> Dict[str, Any]:
    """
    Extract basic metadata from text content
    
    Args:
        text: The text content
        
    Returns:
        Dict with basic metadata
    """
    lines = text.split('\n')
    word_count = len(re.findall(r'\w+', text))
    
    return {
        "word_count": word_count,
        "line_count": len(lines),
        "char_count": len(text)
    }

def chunk_text(text: str, chunk_size: int = 1000) -> List[str]:
    """
    Divide text into smaller chunks
    
    Args:
        text: The text to divide
        chunk_size: Maximum size of each chunk
        
    Returns:
        List of text chunks
    """
    # Split by paragraphs first
    paragraphs = text.split('\n\n')
    chunks = []
    current_chunk = ""
    
    for para in paragraphs:
        if len(current_chunk) + len(para) < chunk_size:
            current_chunk += para + "\n\n"
        else:
            # If current chunk is not empty, add it to chunks
            if current_chunk:
                chunks.append(current_chunk.strip())
            
            # Start a new chunk
            if len(para) > chunk_size:
                # If paragraph is too large, split it further
                words = para.split()
                current_chunk = ""
                
                for word in words:
                    if len(current_chunk) + len(word) < chunk_size:
                        current_chunk += word + " "
                    else:
                        chunks.append(current_chunk.strip())
                        current_chunk = word + " "
            else:
                current_chunk = para + "\n\n"
    
    # Add the last chunk if not empty
    if current_chunk:
        chunks.append(current_chunk.strip())
        
    return chunks