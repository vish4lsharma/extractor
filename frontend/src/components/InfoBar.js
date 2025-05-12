import React from 'react';
import './InfoBar.css';

/**
 * InfoBar component to display document information
 * 
 * @param {Object} props
 * @param {Object} props.documentInfo - Information about the current document
 */
const InfoBar = ({ documentInfo }) => {
  // If no document is loaded, show a message
  if (!documentInfo || !documentInfo.name) {
    return (
      <div className="info-bar info-bar-empty">
        <p>No document loaded. Please upload a document to begin.</p>
      </div>
    );
  }

  // Display document information
  return (
    <div className="info-bar">
      <div className="info-item">
        <span className="info-label">Filename:</span>
        <span className="info-value">{documentInfo.name}</span>
      </div>
      
      <div className="info-item">
        <span className="info-label">Type:</span>
        <span className="info-value">{documentInfo.type}</span>
      </div>
      
      <div className="info-item">
        <span className="info-label">Size:</span>
        <span className="info-value">{formatFileSize(documentInfo.size)}</span>
      </div>
      
      {documentInfo.pages && (
        <div className="info-item">
          <span className="info-label">Pages:</span>
          <span className="info-value">{documentInfo.pages}</span>
        </div>
      )}
      
      {documentInfo.lastModified && (
        <div className="info-item">
          <span className="info-label">Modified:</span>
          <span className="info-value">{formatDate(documentInfo.lastModified)}</span>
        </div>
      )}
    </div>
  );
};

/**
 * Format file size in bytes to a human-readable format
 * 
 * @param {number} bytes - File size in bytes
 * @returns {string} Formatted file size
 */
const formatFileSize = (bytes) => {
  if (!bytes) return '0 Bytes';
  
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
  const i = Math.floor(Math.log(bytes) / Math.log(1024));
  
  return `${(bytes / Math.pow(1024, i)).toFixed(2)} ${sizes[i]}`;
};

/**
 * Format date to a human-readable format
 * 
 * @param {number|string|Date} date - Date to format
 * @returns {string} Formatted date
 */
const formatDate = (date) => {
  if (!date) return '';
  
  const dateObj = new Date(date);
  return dateObj.toLocaleString();
};

export default InfoBar;