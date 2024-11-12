import React, { useState, useEffect } from 'react';
import DataTable from './components/DataTable';
import Filter from './components/Filter';
import Chart from './components/Chart';

function App() {
    const [data, setData] = useState([]);
    const [filter, setFilter] = useState({ survived: '' });

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch('/data.json');
                if (!response.ok) {
                    throw new Error('Error while loading the JSON file');
                }
                const jsonData = await response.json();

                
                const filteredData = jsonData.filter(item => {
                    if (filter.survived !== '') {
                        return item.Survived === parseInt(filter.survived);
                    }
                    return true; 
                });

                setData(filteredData); 
            } catch (error) {
                console.error('Erreur:', error);
            }
        };

        fetchData();
    }, [filter]); 
    return (
        <div>
            <Filter setFilter={setFilter} />
            <DataTable data={data} />
            <Chart data={data} />
        </div>
    );
}

export default App;
