const express = require('express');
const router = express.Router();
const Project = require('../models/project');

// GET /api/projects
router.get('/', async (req, res) => {
  try {
    const projects = await Project.find();
    res.json(projects);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

module.exports = router;
