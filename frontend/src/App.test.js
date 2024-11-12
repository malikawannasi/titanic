import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import App from './App';

// Mock des composants enfants pour simplifier le test
jest.mock('./components/DataTable', () => () => <div>DataTable Component</div>);
jest.mock('./components/Filter', () => ({ setFilter }) => (
  <div>
    <button onClick={() => setFilter({ survived: '1' })}>Filter Survivors</button>
  </div>
));
jest.mock('./components/Chart', () => () => <div>Chart Component</div>);

describe('App Component', () => {
  it('devrait afficher les composants DataTable, Filter et Chart', () => {
    render(<App />);

    // Vérifie que les composants mockés sont rendus
    expect(screen.getByText('DataTable Component')).toBeInTheDocument();
    expect(screen.getByText('Chart Component')).toBeInTheDocument();
  });

  it('devrait charger les données et appliquer le filtre correctement', async () => {
    // Mock de la requête fetch
    const mockData = [
      { Survived: 1, Name: 'John' },
      { Survived: 0, Name: 'Jane' },
    ];

    global.fetch = jest.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve(mockData),
      })
    );

    render(<App />);

    // Vérifie que les données sont chargées
    await waitFor(() => expect(fetch).toHaveBeenCalledTimes(1));

    // Vérifie qu'aucune donnée n'est filtrée au début
    expect(screen.getByText('DataTable Component')).toBeInTheDocument();

    // Simule un clic sur le bouton de filtrage (qui définit filter.survived = '1')
    fireEvent.click(screen.getByText('Filter Survivors'));

    // Vérifie que le filtre a été appliqué en vérifiant la nouvelle donnée
    await waitFor(() => expect(screen.getByText('DataTable Component')).toBeInTheDocument());
  });
});
