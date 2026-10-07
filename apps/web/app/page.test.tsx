import { render, screen } from '@testing-library/react';
import HomePage from './page';

describe('HomePage', () => {
  it('renders the ImóvelRadar heading', () => {
    render(<HomePage />);

    expect(screen.getByRole('heading', { name: /imóvelradar/i })).toBeInTheDocument();
  });
});
