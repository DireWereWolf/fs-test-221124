// server.js
const express = require('express');
const path = require('path');
require('dotenv').config();  // Load environment variables from .env

const app = express();

// Set up the environment variables for host and port
const host = process.env.HOST || '0.0.0.0';
const port = process.env.PORT || 9000;

// Debug: Log the path to the static files
console.log('Serving static files from: ', path.join(__dirname, 'dist', 'fe', 'browser'));


// Serve static files from the dist/fe/browser directory
app.use(express.static(path.join(__dirname, 'dist', 'fe', 'browser')));

// Wildcard route to serve the index.html
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'dist', 'fe', 'browser', 'index.html'), (err) => {
    if (err) {
      console.error('Error sending index.html:', err);
      res.status(500).send('Error serving the index.html');
    }
  });
});

// Start the server
app.listen(port, host, () => {
  console.log(`Server is running at http://${host}:${port}`);
});
