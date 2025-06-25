const mongoose = require('mongoose');

const employeeSchema = new mongoose.Schema({
    name: { type: String, required: true },
    phone: { type: Number, required: true },
    employee_id: { type: String, required: true, unique: true },
    tasks: [{ type: mongoose.Schema.Types.ObjectId, ref: 'Task' }],
    projects: [{ type: mongoose.Schema.Types.ObjectId, ref: 'Project' }]
}, {
    timestamps: true
});

const Employee = mongoose.model('Employee', employeeSchema);

module.exports = Employee;