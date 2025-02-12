import { useState, useEffect } from 'react';
import API from '../api';
import TaskList from './TaskList';
import AddTask from './AddTask';
import Protected from './Protected';
import Login from './Login';

function App() {
  const [tasks, setTasks] = useState([]);

  useEffect(() => {
    API.get('/tasks')
      .then(response => setTasks(response.data))
      .catch(error => console.error('Ошибка при загрузке задач:', error));
  }, []);

  const handleTaskAdded = (newTask) => {
    setTasks((prevTasks) => {
      const updatedTasks = [...prevTasks, newTask]; // Добавляем новую задачу в массив
      console.info(updatedTasks); // Логируем обновлённый массив задач
      return updatedTasks;
    });
  };

  const handleLogined = () => {
    console.info('Успешно вошли');
  };

  return (
    <div>
      <h1>Список задач</h1>
      <AddTask onTaskAdded={handleTaskAdded} />
      <TaskList tasks={tasks} setTasks={setTasks} />

      <h2>Закрытая область</h2>
      <Protected />
      <Login onLogin={handleLogined} />
    </div>
  );
}

export default App;
