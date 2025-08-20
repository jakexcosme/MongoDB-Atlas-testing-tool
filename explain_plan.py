#!/usr/bin/env python3
"""
MongoDB Atlas Explain Plan Analysis Script
Analyzes query performance using MongoDB explain plans.
"""

import os
from pymongo import MongoClient
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()

def analyze_query_performance(collection, query, description="Query"):
    """Analyze query performance using explain plan"""
    print(f"\n🔍 Analyzing: {description}")
    print(f"Query: {query}")
    
    explain_result = collection.find(query).explain()
    
    execution_stats = explain_result.get('executionStats', {})
    
    print(f"📊 Performance Metrics:")
    print(f"   • Execution Time: {execution_stats.get('executionTimeMillis', 0)}ms")
    print(f"   • Documents Examined: {execution_stats.get('totalDocsExamined', 0)}")
    print(f"   • Documents Returned: {execution_stats.get('totalDocsReturned', 0)}")
    print(f"   • Index Used: {execution_stats.get('totalKeysExamined', 0) > 0}")
    
    winning_plan = explain_result.get('queryPlanner', {}).get('winningPlan', {})
    stage = winning_plan.get('stage', '')
    
    if stage == 'COLLSCAN':
        print("⚠️  WARNING: Full collection scan detected!")
        print("   Consider adding an index for better performance")
    elif stage == 'IXSCAN':
        print("✅ Index scan used - good performance")
    
    docs_examined = execution_stats.get('totalDocsExamined', 0)
    docs_returned = execution_stats.get('totalDocsReturned', 0)
    
    if docs_examined > 0:
        efficiency = (docs_returned / docs_examined) * 100
        print(f"📈 Query Efficiency: {efficiency:.2f}%")
        
        if efficiency < 10:
            print("⚠️  Low efficiency - consider optimizing query or adding indexes")
        elif efficiency > 50:
            print("✅ Good query efficiency")
    
    return explain_result

def run_explain_plan_tests():
    """Run various queries and analyze their explain plans"""
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
        
        count = collection.count_documents({})
        if count == 0:
            print("⚠️  No documents found. Run upload_documents.py first.")
            return False
        
        print(f"📊 Analyzing queries on {count} documents")
        
        test_queries = [
            ({"email": "user1@example.com"}, "Email lookup (no index)"),
            ({"status": "active"}, "Status filter (no index)"),
            ({"department": "Engineering"}, "Department filter (no index)"),
            ({"salary": {"$gte": 100000}}, "Salary range query (no index)"),
            ({"location": "New York", "status": "active"}, "Compound query (no index)"),
            ({"profile.age": {"$gte": 30, "$lte": 40}}, "Nested field range query"),
        ]
        
        for query, description in test_queries:
            analyze_query_performance(collection, query, description)
        
        print("\n💡 Suggested Indexes for Better Performance:")
        print("   db.test_collection.createIndex({\"email\": 1}, {\"unique\": true})")
        print("   db.test_collection.createIndex({\"status\": 1})")
        print("   db.test_collection.createIndex({\"department\": 1})")
        print("   db.test_collection.createIndex({\"salary\": 1})")
        print("   db.test_collection.createIndex({\"location\": 1, \"status\": 1})")
        print("   db.test_collection.createIndex({\"profile.age\": 1})")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ Error running explain plan analysis: {e}")
        return False

if __name__ == "__main__":
    success = run_explain_plan_tests()
    exit(0 if success else 1)
