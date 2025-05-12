import React, { useState } from 'react';
import ApiService from './api/api'; // Importing ApiService

const DocumentExtractionApp = () => {
    const [file, setFile] = useState(null);
    const [taskId, setTaskId] = useState(null);
    const [status, setStatus] = useState(null);
    const [error, setError] = useState(null);

    // Handle file upload
    const handleFileUpload = async (e) => {
        const uploadedFile = e.target.files[0];
        setFile(uploadedFile);
        
        try {
            const response = await ApiService.uploadDocument(uploadedFile);
            setTaskId(response.task_id);
            console.log('File uploaded, Task ID:', response.task_id);
        } catch (error) {
            setError('Error uploading the file.');
        }
    };

    // Get extraction status
    const checkExtractionStatus = async () => {
        if (!taskId) {
            setError('Please upload a document first.');
            return;
        }

        try {
            const response = await ApiService.getExtractionStatus(taskId);
            setStatus(response.status);
            console.log('Extraction status:', response.status);
        } catch (error) {
            setError('Error fetching extraction status.');
        }
    };

    // Delete task and associated files
    const handleDeleteTask = async () => {
        if (!taskId) {
            setError('Please upload a document first.');
            return;
        }

        try {
            const response = await ApiService.deleteTask(taskId);
            setStatus(null);
            setTaskId(null);
            console.log('Task deleted:', response);
        } catch (error) {
            setError('Error deleting the task.');
        }
    };

    return (
        <div className="document-extraction-app">
            <h1>Document Extraction</h1>
            <input type="file" onChange={handleFileUpload} />
            
            {file && <p>Selected file: {file.name}</p>}

            <button onClick={checkExtractionStatus}>Check Status</button>
            <button onClick={handleDeleteTask}>Delete Task</button>
            
            {status && <p>Task Status: {status}</p>}
            {error && <p style={{ color: 'red' }}>{error}</p>}
        </div>
    );
};

export default DocumentExtractionApp;
