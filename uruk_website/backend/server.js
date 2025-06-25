const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

// Connect to MongoDB
mongoose.connect('mongodb://localhost:27017/Uruk', {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});

// Routes
const projectsRouter = require('./routes/projects');
app.use('/api/projects', projectsRouter);

const employeesRouter = require('./routes/employees');
app.use('/api/employees', employeesRouter);

// Start server
const PORT = 5000;
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
