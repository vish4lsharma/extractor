import logging
from typing import Dict, Any, List
import os

# Import the necessary libraries for PDF extraction
try:
    import PyPDF2
    from PyPDF2 import PdfReader
except ImportError:
    logging.warning("PyPDF2 not installed. PDF extraction will not work.")

class PDFExtractor:
    """Extract content from PDF files"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def extract(self, file_path: str) -> Dict[str, Any]:
        """
        Extract text and metadata from a PDF file
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Dict containing extracted content and metadata
        """
        self.logger.info(f"Extracting content from PDF: {file_path}")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"PDF file not found: {file_path}")
        
        try:
            # Open the PDF
            with open(file_path, 'rb') as file:
                reader = PdfReader(file)
                
                # Extract metadata
                metadata = {}
                if reader.metadata:
                    for key in reader.metadata:
                        if key and reader.metadata[key]:
                            # Convert from PDF internal format to regular string if needed
                            try:
                                value = reader.metadata[key]
                                if isinstance(value, str):
                                    metadata[key] = value
                                else:
                                    metadata[key] = str(value)
                            except:
                                pass
                
                # Extract text content from each page
                num_pages = len(reader.pages)
                content = []
                
                for i in range(num_pages):
                    page = reader.pages[i]
                    content.append(page.extract_text())
                
                # Combine all pages into a single string
                combined_content = "\n\n".join(content)
                
                result = {
                    "content": combined_content,
                    "page_count": num_pages,
                    "metadata": metadata,
                }
                
                self.logger.info(f"Successfully extracted {num_pages} pages from {file_path}")
                return result
                
        except Exception as e:
            self.logger.error(f"PDF extraction failed: {str(e)}")
            raise ValueError(f"Failed to extract content from PDF: {str(e)}")
    
    def extract_page(self, file_path: str, page_num: int) -> str:
        """
        Extract text from a specific page of a PDF
        
        Args:
            file_path: Path to the PDF file
            page_num: Page number to extract (0-indexed)
            
        Returns:
            The extracted text from the specified page
        """
        with open(file_path, 'rb') as file:
            reader = PdfReader(file)
            
            if page_num < 0 or page_num >= len(reader.pages):
                raise ValueError(f"Invalid page number: {page_num}")
            
            page = reader.pages[page_num]
            return page.extract_text()