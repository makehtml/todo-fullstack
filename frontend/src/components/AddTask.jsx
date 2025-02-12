import { useState } from 'react';
import API from '../api';

function AddTask({ onTaskAdded }) {
  const [title, setTitle] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await API.post('/tasks', { title });
      onTaskAdded(response.data);
      setTitle('');
    } catch (error) {
      console.error('Ошибка при добавлении задачи:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="Введите задачу"
      />
      <button type="submit">Добавить</button>
    </form>
  );
}

export default AddTask;
