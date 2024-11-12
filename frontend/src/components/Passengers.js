import React, { useEffect, useState } from 'react';

const Passengers = () => {
    const [passengers, setPassengers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchPassengers = async () => {
            try {
                const response = await fetch('/data.json');
                if (!response.ok) {
                    throw new Error('Error while loading the JSON file');
                }
                const data = await response.json(); 
                setPassengers(data); 
            } catch (error) {
                setError('Error while loading data');
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
