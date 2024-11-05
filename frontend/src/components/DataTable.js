import React from 'react';

function DataTable({ data }) {
    return (
        <table>
            <thead>
                <tr>
                    <th>Passenger ID</th>
                    <th>Survived</th>
                    <th>Pclass</th>
                    <th>Name</th>
                    <th>Sex</th>
                    <th>Age</th>
                    <th>SibSp</th>
                    <th>Parch</th>
                    <th>Ticket</th>
                    <th>Fare</th>
                </tr>
            </thead>
            <tbody>
                {data.map(passenger => (
                    <tr key={passenger.PassengerId}>
                        <td>{passenger.PassengerId}</td>
                        <td>{passenger.Survived}</td>
                        <td>{passenger.Pclass}</td>
                        <td>{passenger.Name}</td>
                        <td>{passenger.Sex}</td>
                        <td>{passenger.Age}</td>
                        <td>{passenger.SibSp}</td>
                        <td>{passenger.Parch}</td>
                        <td>{passenger.Ticket}</td>
                        <td>{passenger.Fare}</td>
                    </tr>
                ))}
            </tbody>
        </table>
    );
}

export default DataTable;
