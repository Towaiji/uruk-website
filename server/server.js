import express from 'express';
import { MongoClient } from 'mongodb';
import dotenv from 'dotenv';
import path from 'path';
import { fileURLToPath } from 'url';

// allow environment variables from .env
dotenv.config();

const app = express();
const port = process.env.PORT || 3000;

const mongoUri = process.env.MONGO_URI;
if (!mongoUri) {
  console.error('Missing MONGO_URI environment variable');
  process.exit(1);
}

let client;
async function connect() {
  client = new MongoClient(mongoUri);
  await client.connect();
  console.log('Connected to MongoDB');
}
connect().catch((err) => {
  console.error('Failed to connect to MongoDB:', err);
  process.exit(1);
});

// simple endpoint to list projects
app.get('/api/projects', async (req, res) => {
  try {
    const db = client.db();
    const projects = await db.collection('projects').find({}).toArray();
    res.json(projects);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Database error' });
  }
});

// serve static site from uruk_website folder
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
app.use(express.static(path.join(__dirname, '../uruk_website')));

app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
