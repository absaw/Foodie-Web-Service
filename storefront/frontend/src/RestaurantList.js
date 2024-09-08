import React from 'react';

function RestaurantList({ restaurants }) {
  if (restaurants.length === 0) {
    return null;
  }

  return (
    <div className="restaurant-list">
      <h2>Top Restaurants Near You</h2>
      <ul>
        {restaurants.map((restaurant) => (
          <li key={restaurant.id}>
            <h3>{restaurant.name}</h3>
            <p>Rating: {restaurant.rating}</p>
            <p>{restaurant.location.address1}, {restaurant.location.city}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default RestaurantList;