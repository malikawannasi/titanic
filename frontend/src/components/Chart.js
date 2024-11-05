import React from 'react';
import { Bar } from 'react-chartjs-2';

function Chart({ data }) {
    const chartData = {
        labels: data.map(p => p.name),
        datasets: [
            {
                label: 'Fare',
                data: data.map(p => p.fare),
                backgroundColor: 'rgba(75, 192, 192, 0.6)'
            }
        ]
    };

    return <Bar data={chartData} />;
}

export default Chart;
