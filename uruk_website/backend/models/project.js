const mongoose = require('mongoose');

const employeeSchema = new mongoose.Schema({
    name: { type: String, required: true },
    client: { type: String, required: true },
    members: [{ type: mongoose.Schema.Types.ObjectId, ref: 'Employee' }],
    location: { type: String, required: true },
    description: { type: String, required: true }
}, {
    timestamps: true 
});

const Project = mongoose.model('Project', projectSchema);

module.exports = Project;
