from typing import Dict, Any, Optional
import os
import logging
from enum import Enum

from ..extractors.pdf_extractor import PDFExtractor
from ..extractors.image_extractor import ImageExtractor
from ..extractors.excel_extractor import ExcelExtractor
from ..models.models import ExtractorType

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DataExtractionApp:
    """Main class for document extraction functionality"""
    
    def __init__(self):
        """Initialize the data extraction application"""
        self.extractors = {
            ExtractorType.PDF: PDFExtractor(),
            ExtractorType.IMAGE: ImageExtractor(),
            ExtractorType.EXCEL: ExcelExtractor(),
        }
        logger.info("DataExtractionApp initialized")
    
    def extract(self, file_path: str, extractor_type: Optional[ExtractorType] = None) -> Dict[str, Any]:
        """
        Extract content from a document
        
        Args:
            file_path: Path to the document file
            extractor_type: The type of extractor to use. If None, determined from file extension.
            
        Returns:
            Dict containing extraction results (content, metadata, etc.)
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Determine extractor type if not provided
        if extractor_type is None:
            extractor_type = self._determine_extractor_type(file_path)
        
        logger.info(f"Extracting content from {file_path} using {extractor_type.value} extractor")
        
        # Get the appropriate extractor
        extractor = self.extractors.get(extractor_type)
        if not extractor:
            raise ValueError(f"No extractor available for type: {extractor_type}")
        
        # Perform extraction
        try:
            result = extractor.extract(file_path)
            logger.info(f"Successfully extracted content from {file_path}")
            return result
        except Exception as e:
            logger.error(f"Extraction failed for {file_path}: {str(e)}")
            raise
    
    def _determine_extractor_type(self, file_path: str) -> ExtractorType:
        """Determine the appropriate extractor type based on file extension"""
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        
        if ext in ['.pdf']:
            return ExtractorType.PDF
        elif ext in ['.jpg', '.jpeg', '.png', '.tiff', '.bmp']:
            return ExtractorType.IMAGE
        elif ext in ['.xlsx', '.xls', '.csv']:
            return ExtractorType.EXCEL
        else:
            raise ValueError(f"Unsupported file extension: {ext}")
    
    def get_supported_formats(self) -> Dict[str, list]:
        """Get all supported file formats by extractor type"""
        return {
            "pdf": [".pdf"],
            "image": [".jpg", ".jpeg", ".png", ".tiff", ".bmp"],
            "excel": [".xlsx", ".xls", ".csv"]
        }