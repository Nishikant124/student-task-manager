// 1. Select the DOM elements we need to interact with
const taskInput = document.getElementById('taskInput');
const addBtn = document.getElementById('addBtn');
const taskList = document.getElementById('taskList');

// 2. Load tasks as soon as the page opens
window.onload = function() {
    fetchTasks();
};

// 3. Add Event Listener to the Button
addBtn.addEventListener('click', function() {
    const taskText = taskInput.value;

    if (taskText === "") {
        alert("Please enter a task!");
        return;
    }

    addTask(taskText);
});

// --- CORE FUNCTIONS ---

// Function A: Get tasks from Backend and show them
function fetchTasks() {
    fetch('/tasks') // Calls the GET API
        .then(response => response.json()) // Converts "text" response to JSON object
        .then(data => {
            taskList.innerHTML = ""; // Clear current list to avoid duplicates
            
            // Loop through every task and add it to the screen
            data.forEach(task => {
                const li = document.createElement('li');
                li.textContent = task.text; // Use the 'text' field from our JSON
                taskList.appendChild(li);
            });
        })
        .catch(error => console.error('Error loading tasks:', error));
}

// Function B: Send new task to Backend
function addTask(taskText) {
    fetch('/add-task', { // Calls the POST API
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ task: taskText }) // Send data as JSON string
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            // Task added successfully!
            taskInput.value = ""; // Clear the input box
            fetchTasks(); // Refresh the list to show the new item
        }
    })
    .catch(error => console.error('Error adding task:', error));
}