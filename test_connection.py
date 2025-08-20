#!/usr/bin/env python3
"""
MongoDB Atlas Connection Testing Script
Tests basic connectivity and authentication to MongoDB Atlas cluster.
"""

import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from dotenv import load_dotenv

load_dotenv()

def test_connection():
    """Test MongoDB Atlas connection"""
    uri = os.getenv('MONGODB_URI')
    if not uri:
        print("❌ MONGODB_URI not found in environment variables")
        return False
    
    try:
        print("🔗 Testing MongoDB Atlas connection...")
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        
        client.admin.command('ping')
        print("✅ Connection successful!")
        
        server_info = client.server_info()
        print(f"📊 MongoDB version: {server_info['version']}")
        
        databases = client.list_database_names()
        print(f"📁 Available databases: {databases}")
        
        client.close()
        return True
        
    except ConnectionFailure as e:
        print(f"❌ Connection failed: {e}")
        return False
    except ServerSelectionTimeoutError as e:
        print(f"❌ Server selection timeout: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = test_connection()
    exit(0 if success else 1)
