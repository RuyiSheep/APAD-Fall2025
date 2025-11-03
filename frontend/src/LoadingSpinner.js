import React from 'react';

function LoadingSpinner() {
  const style = {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    padding: '16px',
    fontSize: '18px',
    color: '#007bff'
  };
  return <div style={style}>Loading...</div>;
}

export default LoadingSpinner;
