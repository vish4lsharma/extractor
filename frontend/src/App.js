import React from 'react';
import './App.css';
import DocumentExtractionApp from './DocumentExtractionApp';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Document Extraction App</h1>
      </header>
      <main>
        <DocumentExtractionApp />
      </main>
      <footer className="App-footer">
        <p>&copy; 2025 Document Extraction App</p>
      </footer>
    </div>
  );
}

export default App;