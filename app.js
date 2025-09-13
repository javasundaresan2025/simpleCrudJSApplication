const express = require('express');
const app = express();
const PORT = 3000;

app.use(express.json());


app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, DELETE, OPTIONS');
  res.header('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  
  // Handle preflight requests
  if (req.method === 'OPTIONS') {
    res.sendStatus(200);
  } else {
    next();
  }
});



let users = [
  { id: 1, name: 'John Doe', email: 'john@example.com', age: 30 },
  { id: 2, name: 'Jane Smith', email: 'jane@example.com', age: 25 },
  { id: 3, name: 'Bob Johnson', email: 'bob@example.com', age: 35 }
];

let nextId = 4;



/**
 * Get HTTP Method
 */
app.get('/users', (req, res) => {
    console.log("Inside get");

      res.json({
    success: true,
    data: users,
    count: users.length
  });
});

/**
 * Get Particular User
 */
app.get('/users/:id', (req, res) => {
  const user = findUserById(req.params.id);
  
  if (!user) {
    return res.status(404).json({
      success: false,
      message: 'User not found'
    });
  }
  
  res.json({
    success: true,
    data: user
  });
});


/**
 * Post HTTP Method
 */
app.post('/users', (req, res) => {
  const { name, email, age } = req.body;

  const newUser = {
    id: nextId++,
    name,
    email,
    age: parseInt(age)
  };
  
  users.push(newUser);
  
  res.status(201).json({
    success: true,
    message: 'User created successfully',
    data: newUser
  });
});

/**
 * Put HTTP Method
 */
app.put('/users/:id', (req, res) => {
  const user = findUserById(req.params.id);
  
  if (!user) {
    return res.status(404).json({
      success: false,
      message: 'User not found'
    });
  }
  
  const { name, email, age } = req.body;
  
  
  if (!name || !email || !age) {
    return res.status(400).json({
      success: false,
      message: 'Name, email, and age are required'
    });
  }
  
  // Check if email already exists (excluding current user)
  const existingUser = users.find(u => u.email === email && u.id !== user.id);
  if (existingUser) {
    return res.status(400).json({
      success: false,
      message: 'Email already exists'
    });
  }
  
  // Update user properties
  user.name = name;
  user.email = email;
  user.age = parseInt(age);
  
  res.json({
    success: true,
    message: 'User updated successfully',
    data: user
  });
});

/**
 * Find Method
 */
const findUserById = (id) => users.find(user => user.id === parseInt(id));



// DELETE user (Delete)
app.delete('/users/:id', (req, res) => {
  const userIndex = users.findIndex(user => user.id === parseInt(req.params.id));
  
  if (userIndex === -1) {
    return res.status(404).json({
      success: false,
      message: 'User not found'
    });
  }
  
  const deletedUser = users.splice(userIndex, 1)[0];
  
  res.json({
    success: true,
    message: 'User deleted successfully',
    data: deletedUser
  });
});



// Start server
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
  console.log(`Try the following endpoints:`);
  console.log(`GET    http://localhost:${PORT}/users`);
  console.log(`GET    http://localhost:${PORT}/users/1`);
  console.log(`POST   http://localhost:${PORT}/users`);
  console.log(`PUT    http://localhost:${PORT}/users/1`);
  console.log(`DELETE http://localhost:${PORT}/users/1`);
});

module.exports = app;
