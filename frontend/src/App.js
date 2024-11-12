import React, { useState, useEffect } from 'react';
import DataTable from './components/DataTable';
import Filter from './components/Filter';
import Chart from './components/Chart';
import { getPassengers } from './api/api'; // Import the getPassengers function

function App() {
    const [data, setData] = useState([]);
    const [filter, setFilter] = useState({ survived: '' });

    useEffect(() => {
        const fetchData = async () => {
            try {
                // Attempt to fetch data from the API
                let jsonData = await getPassengers(); 

                if (jsonData.length === 0) {
                    throw new Error('API call failed, using fallback data');
                }

                // Proceed with the fetched data if successful
                const filteredData = jsonData.filter(item => {
                    if (filter.survived !== '') {
                        return item.Survived === parseInt(filter.survived);
                    }
                    return true;
                });

                setData(filteredData); 

            } catch (error) {
                console.error('Error:', error);

                // Fallback to loading data from local data.json if API call fails
              /*  try {
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
                    console.error('Fallback failed:', error);
                }*/
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
