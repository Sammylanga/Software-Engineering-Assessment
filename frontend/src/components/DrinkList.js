import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './DrinkList.css'; 

const DrinkList = () => {
  const [drinks, setDrinks] = useState([]);
  const [personDrinkMap, setPersonDrinkMap] = useState({});

  useEffect(() => {
    const fetchDrinks = async () => {
      try {
        const response = await axios.get('https://www.thecocktaildb.com/api/json/v1/1/search.php?f=a');
        setDrinks(response.data.drinks || []);
      } catch (error) {
        console.error('Failed to fetch drinks:', error);
      }
    };
    fetchDrinks();
  }, []);

  const addDrink = async (drinkId, drink_name, drink_type, alcohol_content, personId) => {
      console.log(personDrinkMap[drinkId])
      try {
        const response = await axios.post(`http://127.0.0.1:8000/patrons/update_drinks/${personId}/`,
          {
            "id_drink": `${drinkId},${personId}`,    
            "drink_name": drink_name,
            "drink_type": drink_type,
            "quantity": 1,
            "alcohol_content": alcohol_content
          }
        );
      } catch (error) {
        console.error('Failed to add drink:', error);
      }
  }

  const handleChangePersonId = (personId, drinkId) => {
    setPersonDrinkMap((prevMap) => ({
      ...prevMap,
      [drinkId]: personId
    }));
  };

  return (
    <div>
      <h2 style={{display : 'flex' , justifyContent: 'center'}}>  All Drinks</h2>
      <ul className="drink-list">
        {drinks.map((drink) => (
          <li key={drink.idDrink} className="drink-item">
            <img src={drink.strDrinkThumb} alt={drink.strDrink} />
            <span> Name    : {drink.strDrink}</span>
            <span> Alcahol : {drink.strAlcoholic}</span>
            <div className='add-drink'>
            <input
                type="text"
                value={personDrinkMap[drink.idDrink] || ''}
                onChange={(e) => handleChangePersonId(e.target.value, drink.idDrink)}
                placeholder="Enter a Patron ID"
            />
            <button onClick={() => addDrink(
              drink.idDrink,
              drink.strDrink,
              drink.strCategory,
              drink.strAlcoholic,
              personDrinkMap[drink.idDrink] )}>Add Drink</button>
          </div>
          </li>
        ))}
    </ul>
    </div>
  );
};

export default DrinkList;