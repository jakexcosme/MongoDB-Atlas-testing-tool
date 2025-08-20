# MongoDB Atlas Testing Tool

A simple collection of Python scripts for testing MongoDB Atlas connections and analyzing query performance using explain plans.

## Features

- Test MongoDB Atlas connection reliability
- Upload test documents to collections
- Run explain plan analysis on queries
- Basic performance monitoring scripts

## Setup

```bash
# Install dependencies
pip install pymongo python-dotenv

# Configure environment
cp .env.example .env
# Edit .env with your MongoDB Atlas connection details
```

## Usage

```bash
# Test connection
python test_connection.py

# Upload test documents
python upload_documents.py

# Run explain plan analysis
python explain_plan.py

# Performance testing
python performance_test.py
```

## Configuration

Create a `.env` file with your MongoDB Atlas credentials:

```
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/
DATABASE_NAME=test_db
COLLECTION_NAME=test_collection
```

## Scripts

- `test_connection.py` - Basic connection testing
- `upload_documents.py` - Upload sample documents for testing
- `explain_plan.py` - Query performance analysis with explain plans
- `performance_test.py` - Basic performance benchmarking
