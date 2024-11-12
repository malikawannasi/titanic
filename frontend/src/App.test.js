import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import App from './App';

// Mocking the components DataTable, Filter, and Chart since we are focusing on App.js
jest.mock('./components/DataTable', () => () => <div>DataTable Component</div>);
jest.mock('./components/Filter', () => ({ setFilter }) => {
    return (
        <button onClick={() => setFilter({ survived: '1' })}>Set Filter</button>
    );
});
jest.mock('./components/Chart', () => () => <div>Chart Component</div>);

// Mock the fetch function to simulate API responses
global.fetch = jest.fn();

// Mock console.error to check if error handling works
beforeEach(() => {
    jest.spyOn(console, 'error').mockImplementation(() => {});
    fetch.mockClear();
});

describe('App Component', () => {
    test('should render App component and its children', () => {
        render(<App />);
        
        // Check if the children components are rendered
        expect(screen.getByText('DataTable Component')).toBeInTheDocument();
        expect(screen.getByText('Chart Component')).toBeInTheDocument();
    });

    test('should fetch and display data on render', async () => {
        // Mock successful fetch
        fetch.mockResolvedValueOnce({
            ok: true,
            json: () => Promise.resolve([{ Survived: 1 }, { Survived: 0 }]),
        });

        render(<App />);

        // Wait for the data fetching to finish and state to update
        await waitFor(() => expect(fetch).toHaveBeenCalledTimes(1));

        // Check if the fetch function is called
        expect(fetch).toHaveBeenCalledWith('/data.json');
    });

    test('should update data when filter is applied', async () => {
        fetch.mockResolvedValueOnce({
            ok: true,
            json: () => Promise.resolve([{ Survived: 1 }, { Survived: 0 }]),
        });

        render(<App />);

        // Simulate clicking the filter button to change the filter
        fireEvent.click(screen.getByText('Set Filter'));

        // Check if the data is updated after filter
        await waitFor(() => {
            expect(fetch).toHaveBeenCalledTimes(2); // fetch should be called again after filter change
        });
    });

    test('should handle fetch error gracefully', async () => {
        // Mock a failed fetch request
        fetch.mockRejectedValueOnce(new Error('Error while loading the JSON file'));

        render(<App />);

        // Wait for the error to be caught
        await waitFor(() => {
            expect(console.error).toHaveBeenCalledWith('Erreur:', expect.any(Error));
        });
    });
});
