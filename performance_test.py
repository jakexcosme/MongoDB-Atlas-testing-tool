#!/usr/bin/env python3
"""
MongoDB Atlas Performance Testing Script
Basic performance benchmarking for MongoDB Atlas operations.
"""

import os
import time
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def measure_query_performance(collection, query, description, iterations=100):
    """Measure query performance over multiple iterations"""
    print(f"\n⏱️  Testing: {description}")
    print(f"Query: {query}")
    print(f"Iterations: {iterations}")
    
    times = []
    
    for i in range(iterations):
        start_time = time.time()
        list(collection.find(query).limit(10))  # Convert cursor to list to ensure execution
        end_time = time.time()
        times.append((end_time - start_time) * 1000)  # Convert to milliseconds
    
    avg_time = sum(times) / len(times)
    min_time = min(times)
    max_time = max(times)
    
    print(f"📊 Results:")
    print(f"   • Average: {avg_time:.2f}ms")
    print(f"   • Min: {min_time:.2f}ms")
    print(f"   • Max: {max_time:.2f}ms")
    
    if avg_time < 10:
        print("✅ Excellent performance")
    elif avg_time < 50:
        print("✅ Good performance")
    elif avg_time < 200:
        print("⚠️  Moderate performance - consider optimization")
    else:
        print("❌ Poor performance - optimization needed")
    
    return {
        'average': avg_time,
        'min': min_time,
        'max': max_time,
        'query': query,
        'description': description
    }

def test_connection_performance():
    """Test connection establishment performance"""
    uri = os.getenv('MONGODB_URI')
    
    print("\n🔗 Testing connection performance...")
    
    connection_times = []
    for i in range(10):
        start_time = time.time()
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        client.close()
        end_time = time.time()
        connection_times.append((end_time - start_time) * 1000)
    
    avg_connection_time = sum(connection_times) / len(connection_times)
    print(f"📊 Average connection time: {avg_connection_time:.2f}ms")
    
    if avg_connection_time < 100:
        print("✅ Fast connection times")
    elif avg_connection_time < 500:
        print("✅ Acceptable connection times")
    else:
        print("⚠️  Slow connection times - check network or cluster location")

def run_performance_tests():
    """Run comprehensive performance tests"""
    uri = os.getenv('MONGODB_URI')
    db_name = os.getenv('DATABASE_NAME', 'test_db')
    collection_name = os.getenv('COLLECTION_NAME', 'test_collection')
    
    if not uri:
        print("❌ MONGODB_URI not found in environment variables")
        return False
    
    try:
        test_connection_performance()
        
        print("🔗 Connecting to MongoDB Atlas for query tests...")
        client = MongoClient(uri)
        db = client[db_name]
        collection = db[collection_name]
        
        count = collection.count_documents({})
        if count == 0:
            print("⚠️  No documents found. Run upload_documents.py first.")
            return False
        
        print(f"📊 Running performance tests on {count} documents")
        
        test_queries = [
            ({"email": "user1@example.com"}, "Single email lookup"),
            ({"status": "active"}, "Status filter"),
            ({"department": "Engineering"}, "Department filter"),
            ({"salary": {"$gte": 100000}}, "Salary range query"),
            ({"location": "New York"}, "Location filter"),
        ]
        
        results = []
        for query, description in test_queries:
            result = measure_query_performance(collection, query, description, 50)
            results.append(result)
        
        print("\n📈 Performance Summary:")
        print("=" * 60)
        for result in results:
            print(f"{result['description']:<30} {result['average']:>8.2f}ms")
        
        slowest = max(results, key=lambda x: x['average'])
        print(f"\n🐌 Slowest query: {slowest['description']} ({slowest['average']:.2f}ms)")
        print("💡 Consider adding indexes for better performance")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ Error running performance tests: {e}")
        return False

if __name__ == "__main__":
    success = run_performance_tests()
    exit(0 if success else 1)
