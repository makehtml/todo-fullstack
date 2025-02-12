import { useEffect, useState } from 'react';
import API from '../api';

function Protected() {
  const [message, setMessage] = useState('');

  useEffect(() => {
    API.get('/protected')
      .then(response => setMessage(response.message))
      .catch((err) => setMessage(`Ошибка доступа, ${JSON.stringify(err.response.data)}`));
  }, []);

  return <p>{message}</p>;
}

export default Protected;
