import { useState, useEffect } from 'react';
import API from '../api';

function TaskList({ tasks, setTasks }) {
  useEffect(() => {
    API.get('/tasks').then(response => setTasks(response.data));
  }, []);

  const toggleTask = async (task) => {
    const updatedTask = { ...task, completed: !task.completed };
    await API.put(`/tasks/${task.id}`, updatedTask);
    setTasks(tasks.map(t => (t.id === task.id ? updatedTask : t)));
  };

  const deleteTask = async (id) => {
    await API.delete(`/tasks/${id}`);
    setTasks(tasks.filter(t => t.id !== id));
  };

  return (
    <div>
      <h2>Список задач</h2>
      <ul>
        {tasks.map(task => (
          <li key={task.id}>
            {task.completed ? '✅' : '❎'} {task.title}
            <button onClick={() => toggleTask(task)}>Изменить</button>
            <button onClick={() => deleteTask(task.id)}>Удалить</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default TaskList;
