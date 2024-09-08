import React, { useState } from 'react';
import { Card, CardContent, CardHeader } from './components/ui/card';
import { Input } from './components/ui/input';
import { Button } from './components/ui/button';
import { MapPin, Star } from 'lucide-react';
import { getCsrfToken } from './utils/csrf-util';

const App = () => {
  const [address, setAddress] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const csrftoken = getCsrfToken();
      const response = await fetch('/api/restaurant/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-CSRFToken': csrftoken,
        },
        body: new URLSearchParams({ address }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Failed to fetch restaurants');
      }

      setResults(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-4xl font-bold mb-8 text-center text-blue-600">Foodie Web Service</h1>
      <div className="flex flex-col md:flex-row gap-8">
        <div className="w-full md:w-1/3">
          <Card>
            <CardHeader>
              <h2 className="text-2xl font-semibold">Find Restaurants</h2>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit}>
                <Input
                  type="text"
                  value={address}
                  onChange={(e) => setAddress(e.target.value)}
                  placeholder="Enter your address"
                  className="mb-4"
                />
                <Button type="submit" disabled={loading} className="w-full">
                  {loading ? 'Searching...' : 'Search'}
                </Button>
              </form>
            </CardContent>
          </Card>
        </div>
        <div className="w-full md:w-2/3">
          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
              {error}
            </div>
          )}
          {results && (
            <div>
              <h2 className="text-2xl font-semibold mb-4">Results for: {results.address}</h2>
              <p className="mb-4">
                <MapPin className="inline-block mr-2" />
                Coordinates: {results.geo_coordinates[0]}, {results.geo_coordinates[1]}
              </p>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {results.restaurants.map((restaurant) => (
                  <Card key={restaurant.id}>
                    <CardContent className="p-4">
                      <h3 className="text-xl font-semibold mb-2">{restaurant.name}</h3>
                      <p className="mb-2">{restaurant.categories.join(', ')}</p>
                      <p className="mb-2">
                        <Star className="inline-block mr-1 text-yellow-400" />
                        {restaurant.rating} ({restaurant.review_count} reviews)
                      </p>
                      <p className="mb-2">{restaurant.location.address1}, {restaurant.location.city}</p>
                      <p>{restaurant.display_phone}</p>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default App;