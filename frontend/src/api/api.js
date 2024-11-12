
import axios from 'axios';

// Function to retrieve passengers
export const getPassengers = async () => {
    try {
        const response = await axios.get('http://localhost:8000/passengers');
        return response.data;
    } catch (error) {
        console.error("Erreur lors de la récupération des passagers:", error);
        throw error;
    }
};
