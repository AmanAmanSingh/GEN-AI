document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('todo-form');
  const input = document.getElementById('todo-input');
  const list = document.getElementById('todo-list');

  form.addEventListener('submit', function(event) {
    event.preventDefault();
    const text = input.value.trim();
    if (text === '') return;
    addTodoItem(text);
    input.value = '';
    input.focus();
  });

  function addTodoItem(text) {
    const li = document.createElement('li');
    li.textContent = text;

    const btn = document.createElement('button');
    btn.className = 'delete-btn';
    btn.textContent = '✖';
    btn.onclick = () => list.removeChild(li);

    li.appendChild(btn);
    list.appendChild(li);
  }
});
