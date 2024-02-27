import React from 'react';
import DrinkList from './components/DrinkList';
import Patron from './components/Patron';

const Main = () => {
  return (
    <div className='main-div' style={{display: 'flex', justifyContent: 'center'}}>
      <DrinkList />
      <Patron />
    </div>
  );
};

export default Main;