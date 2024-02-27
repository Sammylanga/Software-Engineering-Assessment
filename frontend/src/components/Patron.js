// Patron.js

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Patron.css';
import calculateColor from './CalculateColor';

const Patron = () => {
    const [patrons, setPatrons] = useState([]);
    const [patronWeight, setPatronWeight] = useState('');

    const handleDelete = async (index) => {
        try {
          const response = await axios.delete(`http://127.0.0.1:8000/delete_patron/${index}/`);
          const updatePatrons = await axios.get('http://127.0.0.1:8000/all_patrons/');
          setPatrons(updatePatrons.data || []);
         } catch (error) {
          console.error('Failed to delete patrons:', error);
        }
      };

      useEffect(() => {
        const intervalId = setInterval(() => {
          axios.patch('http://127.0.0.1:8000/decrease_consumption/')
            .then((response) => {
                setPatrons(response.data || []);
            })
            .catch((error) => {
              console.error('There was a problem with your PATCH request:', error);
            });
        }, 10000);
    
        return () => clearInterval(intervalId);
      }, []);

    const createPatron = async() => {
        try {
            if ( patronWeight>10 && patronWeight< 500 ) {
                const response = await axios.post(`http://127.0.0.1:8000/patrons/create/`,{  
                "weight" : patronWeight
               });
               const updatePatrons = await axios.get('http://127.0.0.1:8000/all_patrons/');
               setPatrons(updatePatrons.data || []);
            }
          } catch (error) {
            console.error('Failed to create patron:', error);
          }
    }

    useEffect(() => {
        const fetchPatrons = async () => {
          try {
            const response = await axios.get('http://127.0.0.1:8000/all_patrons/');
            setPatrons(response.data || []);
          } catch (error) {
            console.error('Failed to fetch patrons:', error);
          }
        };
        fetchPatrons();
      }, []);

    return (
        <div style={{display: 'inline'}}>
        <h2 style={{height: 'fit-content', textAlign: 'center'}}>List of all Patrons</h2>
        <div className='create-patron'>
        <input
                type="number"
                value={patronWeight}
                onChange={(e) => setPatronWeight(e.target.value)}
                placeholder="Enter a Patron weight"
            />
            <button onClick={() => createPatron()}>Create a patron</button>
        </div>
        <div className='profile-div'>
            {patrons.map((patron) => (
                        <div key={patron.id_patron} className="profile-card" >
                        <div className="profile-header">
                            <div className='face' style={{backgroundColor: calculateColor(patron.consumption)}}>
                            </div>
                            <h2>Patron {patron.id_patron}</h2>
                        </div>
                        <div className='delete-patron'>
                        <button onClick={() => handleDelete(patron.id_patron)}>Delete a Patron</button>
                        </div>
                        <div className="profile-body">
                            <p>Weight: {patron.weight}kg</p>
                            <p>Drinks:</p>
                            <ul className='beers'>
                                {patron.drinks.map((drink) => (
                                    <li key={drink.id_drink}> <span>{drink.drink_name}</span> <span>QTY:{drink.quantity}</span></li>
                                    ))}
                                </ul>
                        </div>
                    </div>
            ))}
            </div>
        </div>
    );
};

export default Patron;
