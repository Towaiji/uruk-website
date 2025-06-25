const express = require('express');
const router = express.Router();
const Employee = require('../models/employee');

// GET /api/employees
router.get('/', async (req, res) => {
  try {
    const employees = await Employee.find();
    res.json(employees);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

module.exports = router;
