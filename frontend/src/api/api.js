import axios from 'axios';

// Configure axios defaults
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

/**
 * API service for document extraction operations
 */
class ApiService {
    /**
     * Upload a document for extraction
     * 
     * @param {File} file - The file to upload
     * @returns {Promise} - API response with task ID
     */
    static async uploadDocument(file) {
        const formData = new FormData();
        formData.append('file', file);
        
        try {
            const response = await api.post('/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            return response.data;
        } catch (error) {
            this.handleError(error);
            throw error;
        }
    }
    
    /**
     * Get extraction status and results for a task
     * 
     * @param {string} taskId - The task ID
     * @returns {Promise} - API response with status and results
     */
    static async getExtractionStatus(taskId) {
        try {
            const response = await api.get(`/status/${taskId}`);
            return response.data;
        } catch (error) {
            this.handleError(error);
            throw error;
        }
    }
    
    /**
     * Delete a task and its associated files
     * 
     * @param {string} taskId - The task ID
     * @returns {Promise} - API response
     */
    static async deleteTask(taskId) {
        try {
            const response = await api.delete(`/tasks/${taskId}`);
            return response.data;
        } catch (error) {
            this.handleError(error);
            throw error;
        }
    }
    
    /**
     * Handle API errors consistently
     * 
     * @param {Error} error - The error object
     */
    static handleError(error) {
        if (error.response) {
            // Server responded with a status code outside of 2xx range
            console.error('API Error:', error.response.data);
        } else if (error.request) {
            // Request was made but no response received
            console.error('Network Error:', error.request);
        } else {
            // Something happened in setting up the request
            console.error('Error:', error.message);
        }
    }
}

export default ApiService;
