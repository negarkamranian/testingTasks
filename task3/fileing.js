const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 3000;

app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'public')));

// Function to generate a random number
function generateRandomNumber(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

// Function to get the current date and time
function getCurrentDateTime() {
  const currentDate = new Date();
  const date = currentDate.toLocaleDateString();
  const time = currentDate.toLocaleTimeString();
  return { date, time };
}

// Function to save the record to a file
function saveRecord(username, minNumber, maxNumber, number, date, time) {
  const record = {
	username,
	minNumber,
	maxNumber,
	number,
	date,
	time
  };

  fs.appendFile('records.txt', JSON.stringify(record) + '\n', (err) => {
	if (err) {
  	console.error('Error saving record:', err);
	}
  });
}

// Function to read records from the file
function loadRecords(username, callback) {
  fs.readFile('records.txt', 'utf8', (err, data) => {
	if (err) {
  	console.error('Error loading records:', err);
  	return callback([]);
	}

	const records = data.split('\n')
  	.filter(line => line.trim() !== '')
  	.map(line => JSON.parse(line));

	const filteredRecords = records.filter(record => record.username === username);
	callback(filteredRecords);
  });
}

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.post('/generate', (req, res) => {
  const username = req.body.username;
  const minNumber = parseInt(req.body.minNumber);
  const maxNumber = parseInt(req.body.maxNumber);

  if (isNaN(minNumber) || isNaN(maxNumber)) {
	return res.status(400).send('Please enter valid numbers.');
  }

  const randomNumber = generateRandomNumber(minNumber, maxNumber);
  const { date, time } = getCurrentDateTime();

  const result = {
	username,
	randomNumber,
	date,
	time
  };

  saveRecord(username, minNumber, maxNumber, randomNumber, date, time);

  res.json(result);
});

app.get('/records/:username', (req, res) => {
  const username = req.params.username;

  loadRecords(username, (records) => {
	res.json(records);
  });
});

app.listen(PORT, () => {
  console.log(`Server is running on port ${80}`);
});



