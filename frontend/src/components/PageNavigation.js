import React from 'react';
import './PageNavigation.css';

/**
 * PageNavigation component for navigating between pages in multi-page documents
 * 
 * @param {Object} props
 * @param {number} props.currentPage - Current page number
 * @param {number} props.totalPages - Total number of pages
 * @param {Function} props.onPageChange - Handler when page is changed
 * @param {boolean} props.disabled - Whether navigation is disabled
 */
const PageNavigation = ({ currentPage, totalPages, onPageChange, disabled }) => {
  // If there's only one page or no pages, don't render anything
  if (!totalPages || totalPages <= 1) {
    return null;
  }

  // Handle going to the previous page
  const handlePrevious = () => {
    if (currentPage > 1 && !disabled) {
      onPageChange(currentPage - 1);
    }
  };

  // Handle going to the next page
  const handleNext = () => {
    if (currentPage < totalPages && !disabled) {
      onPageChange(currentPage + 1);
    }
  };

  // Handle going to a specific page
  const handlePageClick = (page) => {
    if (page !== currentPage && !disabled) {
      onPageChange(page);
    }
  };

  // Create page numbers to display
  const renderPageNumbers = () => {
    const pageNumbers = [];
    const maxVisiblePages = 5;
    
    // Always show first page
    pageNumbers.push(
      <button 
        key={1} 
        className={`page-number ${currentPage === 1 ? 'active' : ''}`}
        onClick={() => handlePageClick(1)}
        disabled={disabled}
      >
        1
      </button>
    );
    
    // If there are many pages, show ellipsis
    if (totalPages > maxVisiblePages) {
      let startPage = Math.max(2, currentPage - 1);
      let endPage = Math.min(startPage + 2, totalPages - 1);
      
      // Adjust start page if we're near the end
      if (endPage === totalPages - 1) {
        startPage = Math.max(2, endPage - 2);
      }
      
      // Show ellipsis at the beginning if needed
      if (startPage > 2) {
        pageNumbers.push(<span key="ellipsis1" className="ellipsis">...</span>);
      }
      
      // Show middle pages
      for (let i = startPage; i <= endPage; i++) {
        pageNumbers.push(
          <button 
            key={i} 
            className={`page-number ${currentPage === i ? 'active' : ''}`}
            onClick={() => handlePageClick(i)}
            disabled={disabled}
          >
            {i}
          </button>
        );
      }
      
      // Show ellipsis at the end if needed
      if (endPage < totalPages - 1) {
        pageNumbers.push(<span key="ellipsis2" className="ellipsis">...</span>);
      }
    } else {
      // Show all pages if there aren't many
      for (let i = 2; i < totalPages; i++) {
        pageNumbers.push(
          <button 
            key={i} 
            className={`page-number ${currentPage === i ? 'active' : ''}`}
            onClick={() => handlePageClick(i)}
            disabled={disabled}
          >
            {i}
          </button>
        );
      }
    }
    
    // Always show last page if there's more than one page
    if (totalPages > 1) {
      pageNumbers.push(
        <button 
          key={totalPages} 
          className={`page-number ${currentPage === totalPages ? 'active' : ''}`}
          onClick={() => handlePageClick(totalPages)}
          disabled={disabled}
        >
          {totalPages}
        </button>
      );
    }
    
    return pageNumbers;
  };

  return (
    <div className="page-navigation">
      <button 
        className="nav-button prev" 
        onClick={handlePrevious} 
        disabled={currentPage === 1 || disabled}
      >
        Previous
      </button>
      
      <div className="page-numbers">
        {renderPageNumbers()}
      </div>
      
      <button 
        className="nav-button next" 
        onClick={handleNext} 
        disabled={currentPage === totalPages || disabled}
      >
        Next
      </button>
    </div>
  );
};

export default PageNavigation;