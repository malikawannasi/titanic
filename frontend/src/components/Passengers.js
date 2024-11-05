import React, { useEffect, useState } from 'react';
import { getPassengers } from '../api/api'; // Importer la fonction pour récupérer les passagers

const Passengers = () => {
    const [passengers, setPassengers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchPassengers = async () => {
            try {
                const data = await getPassengers();
                setPassengers(data); // Mettre à jour l'état avec les données des passagers
            } catch (error) {
                setError('Erreur lors du chargement des données');
            } finally {
                setLoading(false);
            }
        };

        fetchPassengers();
    }, []);

    if (loading) return <p>Loading...</p>;
    if (error) return <p>{error}</p>;

    return (
        <div>
            <h1>Passagers</h1>
            <ul>
                {passengers.map(passenger => (
                    <li key={passenger.PassengerId}>
                        {passenger.Name} - {passenger.Sex}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Passengers;
