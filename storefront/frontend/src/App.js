import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [address, setAddress] = useState('');
  const [restaurants, setRestaurants] = useState([]);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('/api/restaurants/', { address });
      setRestaurants(response.data.restaurants);
      setError('');
    } catch (error) {
      setError('Failed to fetch restaurants');
      console.error('Error:', error);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={address}
          onChange={(e) => setAddress(e.target.value)}
          placeholder="Enter address"
        />
        <button type="submit">Find Restaurants</button>
      </form>
      {error && <p>{error}</p>}
      <ul>
        {restaurants.map((restaurant) => (
          <li key={restaurant.id}>{restaurant.name}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;