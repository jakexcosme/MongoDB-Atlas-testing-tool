#!/usr/bin/env python3
"""
MongoDB Atlas Document Upload Script
Uploads sample documents for testing query performance and explain plans.
"""

import os
from pymongo import MongoClient
from datetime import datetime, timedelta
import random
from dotenv import load_dotenv

load_dotenv()

def generate_sample_documents(count=1000):
    """Generate sample documents for testing"""
    documents = []
    
    departments = ['Engineering', 'Sales', 'Marketing', 'HR', 'Finance']
    locations = ['New York', 'San Francisco', 'London', 'Tokyo', 'Sydney']
    statuses = ['active', 'inactive', 'pending']
    
    for i in range(count):
        doc = {
            'user_id': i + 1,
            'email': f'user{i+1}@example.com',
            'username': f'user_{i+1}',
            'department': random.choice(departments),
            'location': random.choice(locations),
            'status': random.choice(statuses),
            'salary': random.randint(40000, 150000),
            'join_date': datetime.now() - timedelta(days=random.randint(1, 1000)),
            'last_login': datetime.now() - timedelta(days=random.randint(0, 30)),
            'profile': {
                'age': random.randint(22, 65),
                'skills': random.sample(['Python', 'JavaScript', 'MongoDB', 'React', 'Node.js', 'AWS'], 
                                      random.randint(1, 4))
            },
            'metadata': {
                'created_at': datetime.now(),
                'version': 1
            }
        }
        documents.append(doc)
    
    return documents

def upload_documents():
    """Upload sample documents to MongoDB Atlas"""
    uri = os.getenv('MONGODB_URI')
    db_name = os.getenv('DATABASE_NAME', 'test_db')
    collection_name = os.getenv('COLLECTION_NAME', 'test_collection')
    
    if not uri:
        print("❌ MONGODB_URI not found in environment variables")
        return False
    
    try:
        print("🔗 Connecting to MongoDB Atlas...")
        client = MongoClient(uri)
        db = client[db_name]
        collection = db[collection_name]
        
        print("🗑️ Clearing existing documents...")
        collection.delete_many({})
        
        print("📝 Generating sample documents...")
        documents = generate_sample_documents(1000)
        
        print("⬆️ Uploading documents...")
        result = collection.insert_many(documents)
        
        print(f"✅ Successfully uploaded {len(result.inserted_ids)} documents")
        print(f"📊 Collection: {db_name}.{collection_name}")
        
        count = collection.count_documents({})
        print(f"🔢 Total documents in collection: {count}")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ Error uploading documents: {e}")
        return False

if __name__ == "__main__":
    success = upload_documents()
    exit(0 if success else 1)
