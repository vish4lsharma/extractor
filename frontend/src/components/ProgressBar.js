import React from 'react';
import './ProgressBar.css';

/**
 * ProgressBar component for showing extraction progress
 * 
 * @param {Object} props
 * @param {number} props.progress - Progress percentage (0-100)
 * @param {string} props.status - Current status message
 * @param {boolean} props.isVisible - Whether the progress bar is visible
 * @param {string} props.type - Type of progress bar (success, warning, info, danger)
 */
const ProgressBar = ({ progress = 0, status = '', isVisible = false, type = 'info' }) => {
  // If not visible, return null
  if (!isVisible) {
    return null;
  }

  // Ensure progress is between 0 and 100
  const normalizedProgress = Math.min(100, Math.max(0, progress));
  
  // Determine CSS class based on type
  const progressClass = `progress-bar-${type}`;

  return (
    <div className="progress-container">
      <div className="progress-wrapper">
        <div 
          className={`progress-bar ${progressClass}`} 
          style={{ width: `${normalizedProgress}%` }}
        >
          <span className="progress-text">{`${Math.round(normalizedProgress)}%`}</span>
        </div>
      </div>
      
      {status && (
        <div className="progress-status">
          {status}
        </div>
      )}
    </div>
  );
};

export default ProgressBar;