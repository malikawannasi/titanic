
import React, { useState, useEffect } from 'react';
import DataTable from './components/DataTable';
import Filter from './components/Filter';
import Chart from './components/Chart';
import axios from 'axios';

function App() {
    const [data, setData] = useState([]);
    const [filter, setFilter] = useState({ survived: '' });

    useEffect(() => {
        axios.get('/api/passengers', { params: filter }).then(response => {
            setData(response.data);
        });
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
