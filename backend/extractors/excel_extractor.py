import logging
from typing import Dict, Any, List
import os
import json

# Import the necessary libraries for Excel extraction
try:
    import pandas as pd
    import openpyxl
except ImportError:
    logging.warning("pandas or openpyxl not installed. Excel extraction will not work.")

class ExcelExtractor:
    """Extract content from Excel and CSV files"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def extract(self, file_path: str) -> Dict[str, Any]:
        """
        Extract data from an Excel or CSV file
        
        Args:
            file_path: Path to the Excel/CSV file
            
        Returns:
            Dict containing extracted data and metadata
        """
        self.logger.info(f"Extracting content from Excel/CSV: {file_path}")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        try:
            file_ext = os.path.splitext(file_path)[1].lower()
            
            if file_ext == '.csv':
                # Handle CSV
                df = pd.read_csv(file_path)
                metadata = {
                    "format": "CSV",
                    "rows": len(df),
                    "columns": len(df.columns)
                }
                sheets = [{"name": "Sheet1", "data": df.to_dict(orient="records")}]
                sheet_names = ["Sheet1"]
                
            else:
                # Handle Excel
                excel_file = pd.ExcelFile(file_path)
                sheet_names = excel_file.sheet_names
                
                # Extract data from each sheet
                sheets = []
                for sheet_name in sheet_names:
                    df = pd.read_excel(file_path, sheet_name=sheet_name)
                    sheets.append({
                        "name": sheet_name,
                        "data": df.to_dict(orient="records")
                    })
                
                metadata = {
                    "format": file_ext.upper().replace('.', ''),
                    "sheet_count": len(sheet_names),
                    "sheet_names": sheet_names
                }
            
            # Convert the structured data to a readable text format
            content_parts = []
            for sheet in sheets:
                content_parts.append(f"Sheet: {sheet['name']}")
                
                # Convert DataFrame to string representation
                if sheet["data"]:
                    df = pd.DataFrame(sheet["data"])
                    content_parts.append(df.to_string(index=False))
                else:
                    content_parts.append("(Empty sheet)")
                    
                content_parts.append("\n")
            
            content = "\n".join(content_parts)
            
            result = {
                "content": content,
                "page_count": len(sheets),  # Consider each sheet as a page
                "metadata": metadata,
                "structured_data": {
                    "sheets": sheets
                }
            }
            
            self.logger.info(f"Successfully extracted data from {file_path}")
            return result
                
        except Exception as e:
            self.logger.error(f"Excel extraction failed: {str(e)}")
            raise ValueError(f"Failed to extract content from Excel/CSV: {str(e)}")
    
    def extract_sheet(self, file_path: str, sheet_name: str = None) -> Dict[str, Any]:
        """
        Extract data from a specific sheet in an Excel file
        
        Args:
            file_path: Path to the Excel file
            sheet_name: Name of the sheet to extract (None for first sheet)
            
        Returns:
            Dict containing the extracted data from the specified sheet
        """
        # Read the specified sheet from the Excel file
        if sheet_name:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
        else:
            df = pd.read_excel(file_path, sheet_name=0)
            
        return {
            "data": df.to_dict(orient="records"),
            "columns": df.columns.tolist(),
            "rows": len(df)
        }