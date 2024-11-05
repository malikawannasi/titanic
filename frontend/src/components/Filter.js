import React from 'react';

function Filter({ setFilter }) {
    const handleSurvivedChange = (e) => {
        setFilter({ survived: e.target.value });
    };

    return (
        <div>
            <label>
                Survived:
                <select onChange={handleSurvivedChange}>
                    <option value="">All</option>
                    <option value="1">Survived</option>
                    <option value="0">Did not survive</option>
                </select>
            </label>
        </div>
    );
}

export default Filter;
