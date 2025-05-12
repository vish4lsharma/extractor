import React, { useState, useEffect } from 'react';
import './SearchBar.css';

/**
 * SearchBar component for searching within extracted content
 * 
 * @param {Object} props
 * @param {Function} props.onSearch - Handler when search is performed
 * @param {boolean} props.disabled - Whether search is disabled
 * @param {number} props.resultCount - Number of search results
 * @param {Function} props.onNextResult - Handler for navigating to next result
 * @param {Function} props.onPrevResult - Handler for navigating to previous result
 * @param {number} props.currentResult - Current result index
 */
const SearchBar = ({ 
  onSearch, 
  disabled = false, 
  resultCount = 0,
  onNextResult,
  onPrevResult,
  currentResult = 0
}) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [searchOptions, setSearchOptions] = useState({
    caseSensitive: false,
    wholeWord: false,
    regex: false
  });
  
  // Update search term when the input changes
  const handleSearchTermChange = (e) => {
    setSearchTerm(e.target.value);
  };
  
  // Update search options when checkboxes change
  const handleOptionChange = (option) => {
    setSearchOptions({
      ...searchOptions,
      [option]: !searchOptions[option]
    });
  };
  
  // Handle search when button is clicked or Enter is pressed
  const handleSearch = (e) => {
    if (e) {
      e.preventDefault();
    }
    
    if (searchTerm.trim() && onSearch) {
      onSearch(searchTerm, searchOptions);
    }
  };
  
  // Handle Enter key press for search
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Enter' && document.activeElement === document.getElementById('search-input')) {
        handleSearch();
      }
    };
    
    document.addEventListener('keydown', handleKeyDown);
    
    return () => {
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, [searchTerm, searchOptions]);
  
  return (
    <div className="search-bar">
      <form onSubmit={handleSearch} className="search-form">
        <div className="search-input-container">
          <input
            id="search-input"
            type="text"
            className="search-input"
            placeholder="Search in content..."
            value={searchTerm}
            onChange={handleSearchTermChange}
            disabled={disabled}
          />
          <button 
            type="submit" 
            className="search-button"
            disabled={disabled || !searchTerm.trim()}
          >
            Search
          </button>
        </div>
        
        <div className="search-options">
          <label className="option-label">
            <input
              type="checkbox"
              checked={searchOptions.caseSensitive}
              onChange={() => handleOptionChange('caseSensitive')}
              disabled={disabled}
            />
            Case sensitive
          </label>
          
          <label className="option-label">
            <input
              type="checkbox"
              checked={searchOptions.wholeWord}
              onChange={() => handleOptionChange('wholeWord')}
              disabled={disabled}
            />
            Whole word
          </label>
          
          <label className="option-label">
            <input
              type="checkbox"
              checked={searchOptions.regex}
              onChange={() => handleOptionChange('regex')}
              disabled={disabled}
            />
            Regex
          </label>
        </div>
      </form>
      
      {resultCount > 0 && (
        <div className="search-results-nav">
          <span className="results-count">
            {currentResult} of {resultCount} results
          </span>
          
          <div className="results-navigation">
            <button 
              className="nav-button prev" 
              onClick={onPrevResult}
              disabled={currentResult <= 1 || disabled}
            >
              Prev
            </button>
            
            <button 
              className="nav-button next" 
              onClick={onNextResult}
              disabled={currentResult >= resultCount || disabled}
            >
              Next
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default SearchBar;