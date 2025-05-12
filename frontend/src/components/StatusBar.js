import React, { useEffect } from 'react';
import './StatusBar.css';

/**
 * StatusBar component to display system notifications and status
 * 
 * @param {Object} props
 * @param {string} props.status - Status message to display
 * @param {string} props.type - Type of status (success, error, warning, info)
 * @param {boolean} props.isTemporary - Whether the status should auto-clear
 * @param {number} props.duration - Duration in ms before auto-clearing (if temporary)
 * @param {Function} props.onClear - Function to call to clear the status
 */
const StatusBar = ({ 
  status = '', 
  type = 'info', 
  isTemporary = false, 
  duration = 5000,
  onClear 
}) => {
  // Auto-clear temporary status messages
  useEffect(() => {
    let timeoutId;
    
    if (status && isTemporary) {
      timeoutId = setTimeout(() => {
        if (onClear) {
          onClear();
        }
      }, duration);
    }
    
    return () => {
      if (timeoutId) {
        clearTimeout(timeoutId);
      }
    };
  }, [status, isTemporary, duration, onClear]);
  
  // If no status, don't render
  if (!status) {
    return null;
  }
  
  // Determine the appropriate icon based on status type
  const getStatusIcon = () => {
    switch (type) {
      case 'success':
        return '✓';
      case 'error':
        return '✕';
      case 'warning':
        return '⚠';
      case 'info':
      default:
        return 'ℹ';
    }
  };
  
  return (
    <div className={`status-bar status-${type}`}>
      <div className="status-icon">
        {getStatusIcon()}
      </div>
      
      <div className="status-message">
        {status}
      </div>
      
      {onClear && (
        <button className="status-close" onClick={onClear}>
          ×
        </button>
      )}
    </div>
  );
};

export default StatusBar;