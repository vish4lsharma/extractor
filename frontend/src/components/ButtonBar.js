import React from 'react';
import './ButtonBar.css';

/**
 * ButtonBar component that provides action buttons for document operations
 * 
 * @param {Object} props
 * @param {Function} props.onUpload - Handler when upload button is clicked
 * @param {Function} props.onExtract - Handler when extract button is clicked
 * @param {Function} props.onSave - Handler when save button is clicked
 * @param {Function} props.onClear - Handler when clear button is clicked
 * @param {boolean} props.isExtracting - Flag indicating if extraction is in progress
 * @param {boolean} props.hasDocument - Flag indicating if a document is loaded
 * @param {boolean} props.hasExtractedContent - Flag indicating if content has been extracted
 */
const ButtonBar = ({ 
  onUpload, 
  onExtract, 
  onSave, 
  onClear,
  isExtracting,
  hasDocument,
  hasExtractedContent
}) => {
  return (
    <div className="button-bar">
      <button 
        className="btn btn-primary" 
        onClick={onUpload}
        disabled={isExtracting}
      >
        Upload Document
      </button>
      
      <button 
        className="btn btn-success" 
        onClick={onExtract}
        disabled={!hasDocument || isExtracting}
      >
        Extract Content
      </button>
      
      <button 
        className="btn btn-info" 
        onClick={onSave}
        disabled={!hasExtractedContent || isExtracting}
      >
        Save Results
      </button>
      
      <button 
        className="btn btn-danger" 
        onClick={onClear}
        disabled={isExtracting}
      >
        Clear
      </button>
    </div>
  );
};

export default ButtonBar;