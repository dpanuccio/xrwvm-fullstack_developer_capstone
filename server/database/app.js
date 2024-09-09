const express = require('express');
const mongoose = require('mongoose');
const fs = require('fs').promises;  // Use fs.promises for async file operations
const cors = require('cors');
const app = express();
const port = 3030;

app.use(cors());
app.use(require('body-parser').urlencoded({ extended: false }));

// Asynchronously load JSON data from files
let reviews_data, dealerships_data;

(async () => {
  try {
    reviews_data = JSON.parse(await fs.readFile("reviews.json", 'utf8'));
    dealerships_data = JSON.parse(await fs.readFile("dealerships.json", 'utf8'));
  } catch (error) {
    console.error("Error reading JSON files:", error);
  }
})();

// Connect to MongoDB
mongoose.connect("mongodb://mongo_db:27017/", { 'dbName': 'dealershipsDB' })
  .then(() => console.log("Connected to MongoDB"))
  .catch((error) => console.error("MongoDB connection error:", error));

// Import Review and Dealership models
const Reviews = require('./review');
const Dealerships = require('./dealership');

// Insert data into MongoDB (dealerships and reviews)
(async () => {
  try {
    await Reviews.deleteMany({});
    await Reviews.insertMany(reviews_data['reviews']);
    console.log("Reviews data inserted successfully.");

    await Dealerships.deleteMany({});
    await Dealerships.insertMany(dealerships_data['dealerships']);
    console.log("Dealerships data inserted successfully.");
  } catch (error) {
    console.error("Error inserting data:", error);
  }
})();

// Express route to home
app.get('/', (req, res) => {
  res.send("Welcome to the Mongoose API");
});

// Express route to fetch all reviews
app.get('/fetchReviews', async (req, res) => {
  try {
    const documents = await Reviews.find();
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to fetch reviews by a particular dealer
app.get('/fetchReviews/dealer/:id', async (req, res) => {
  try {
    const documents = await Reviews.find({ dealership: req.params.id });
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to fetch all dealerships
app.get('/fetchDealers', async (req, res) => {
  try {
    const dealerships = await Dealerships.find();
    res.json(dealerships);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching dealerships' });
  }
});

// Express route to fetch dealerships by a particular state
app.get('/fetchDealers/:state', async (req, res) => {
  try {
    const dealerships = await Dealerships.find({ state: req.params.state });
    res.json(dealerships);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching dealerships by state' });
  }
});

// Express route to fetch dealership by a particular id
app.get('/fetchDealer/:id', async (req, res) => {
  try {
    const dealership = await Dealerships.findById(req.params.id);
    if (!dealership) {
      return res.status(404).json({ error: 'Dealership not found' });
    }
    res.json(dealership);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching dealership by id' });
  }
});

// Express route to insert review
app.post('/insert_review', express.raw({ type: '*/*' }), async (req, res) => {
  try {
    const data = JSON.parse(req.body);
    const documents = await Reviews.find().sort({ id: -1 });
    let new_id = documents[0]['id'] + 1;

    const review = new Reviews({
      "id": new_id,
      "name": data['name'],
      "dealership": data['dealership'],
      "review": data['review'],
      "purchase": data['purchase'],
      "purchase_date": data['purchase_date'],
      "car_make": data['car_make'],
      "car_model": data['car_model'],
      "car_year": data['car_year'],
    });

    const savedReview = await review.save();
    res.json(savedReview);
  } catch (error) {
    console.log(error);
    res.status(500).json({ error: 'Error inserting review' });
  }
});

// Start the Express server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
