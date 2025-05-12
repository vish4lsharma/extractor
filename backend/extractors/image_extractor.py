import logging
from typing import Dict, Any
import os

# Import the necessary libraries for image extraction
try:
    import pytesseract
    from PIL import Image
except ImportError:
    logging.warning("pytesseract or PIL not installed. Image extraction will not work.")

class ImageExtractor:
    """Extract text content from image files using OCR"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Check if tesseract is installed and configured
        try:
            pytesseract.get_tesseract_version()
        except Exception as e:
            self.logger.warning(f"Tesseract OCR may not be properly installed: {str(e)}")
    
    def extract(self, file_path: str) -> Dict[str, Any]:
        """
        Extract text from an image using OCR
        
        Args:
            file_path: Path to the image file
            
        Returns:
            Dict containing extracted text and metadata
        """
        self.logger.info(f"Extracting content from image: {file_path}")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Image file not found: {file_path}")
        
        try:
            # Open the image
            image = Image.open(file_path)
            
            # Extract metadata
            metadata = {
                "format": image.format,
                "size": f"{image.width}x{image.height}",
                "mode": image.mode
            }
            
            # Perform OCR to extract text
            text = pytesseract.image_to_string(image)
            
            result = {
                "content": text,
                "page_count": 1,  # Images are single-page
                "metadata": metadata,
            }
            
            self.logger.info(f"Successfully extracted text from {file_path}")
            return result
                
        except Exception as e:
            self.logger.error(f"Image extraction failed: {str(e)}")
            raise ValueError(f"Failed to extract content from image: {str(e)}")
    
    def extract_with_layout(self, file_path: str) -> Dict[str, Any]:
        """
        Extract text with layout information from an image
        
        Args:
            file_path: Path to the image file
            
        Returns:
            Dict containing extracted text with layout information
        """
        # Open the image
        image = Image.open(file_path)
        
        # Extract text with layout information
        data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
        
        # Process the OCR data to reconstruct layout
        text_blocks = []
        current_block = ""
        
        for i in range(len(data["text"])):
            # Skip empty text
            if not data["text"][i].strip():
                continue
                
            # If this is a new block, add the previous block to the list
            if data["block_num"][i] != data["block_num"][i-1] and current_block:
                text_blocks.append(current_block.strip())
                current_block = ""
                
            # Add text to current block
            current_block += data["text"][i] + " "
            
        # Add the last block
        if current_block:
            text_blocks.append(current_block.strip())
            
        return {
            "content": "\n\n".join(text_blocks),
            "blocks": text_blocks,
            "raw_data": data
        }