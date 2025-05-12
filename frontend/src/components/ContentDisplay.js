import React from 'react';

const ContentDisplay = ({ content, contentType, searchTerm }) => {
  // Function to highlight search terms in text
  const highlightSearchTerm = (text, term) => {
    if (!term || term.trim() === '' || !text) return text;
    
    const regex = new RegExp(`(${term})`, 'gi');
    const parts = text.split(regex);
    
    return parts.map((part, i) => {
      if (part.toLowerCase() === term.toLowerCase()) {
        return <span key={i} className="search-highlight">{part}</span>;
      }
      return part;
    });
  };

  // Render based on content type
  if (!content) {
    return (
      <div className="content-display">
        <div className="text-display" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', color: '#777' }}>
          No content to display. Upload a document to begin.
        </div>
      </div>
    );
  }

  if (contentType === 'image') {
    return (
      <div className="content-display">
        <div className="image-display">
          <img src={content} alt="Document content" />
        </div>
      </div>
    );
  }

  return (
    <div className="content-display">
      <div className="text-display">
        {searchTerm ? highlightSearchTerm(content, searchTerm) : content}
      </div>
    </div>
  );
};

export default ContentDisplay;