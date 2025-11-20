#!/usr/bin/env python3
"""
Quick test script to verify all new features are working
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.database import Database
from src.auth import AuthManager
from src.user_manager import UserManager
from src.order_manager import OrderManager
from src.analytics import Analytics
from src.export import ReportExporter


def test_connection():
    """Test database connection"""
    print("=" * 60)
    print("TEST 1: Database Connection")
    print("=" * 60)
    
    try:
        db = Database()
        if db.connect():
            print("✓ Database connected successfully!")
            db.disconnect()
            return True
        else:
            print("✗ Failed to connect to database")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_auth():
    """Test authentication system"""
    print("\n" + "=" * 60)
    print("TEST 2: Authentication System")
    print("=" * 60)
    
    try:
        db = Database()
        db.connect()
        auth = AuthManager(db)
        
        # Try to login as admin
        print("Testing admin login...")
        success, message = auth.login("admin", "admin123")
        
        if success:
            print("✓ Admin login successful!")
            print(f"✓ Logged in as: {auth.get_current_user().full_name}")
            print(f"✓ Role: {auth.get_current_user().role}")
            auth.logout()
            print("✓ Logout successful!")
            db.disconnect()
            return True
        else:
            print(f"✗ Login failed: {message}")
            db.disconnect()
            return False
            
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_user_manager():
    """Test user management"""
    print("\n" + "=" * 60)
    print("TEST 3: User Management")
    print("=" * 60)
    
    try:
        db = Database()
        db.connect()
        user_mgr = UserManager(db)
        
        # Get user statistics
        print("Getting user statistics...")
        stats = user_mgr.get_user_statistics()
        
        if stats:
            print(f"✓ Total users: {stats.get('total_users', 0)}")
            print(f"✓ Admins: {stats.get('admins', 0)}")
            print(f"✓ Sellers: {stats.get('sellers', 0)}")
            print(f"✓ Customers: {stats.get('customers', 0)}")
            db.disconnect()
            return True
        else:
            print("✗ Failed to get statistics")
            db.disconnect()
            return False
            
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_analytics():
    """Test analytics"""
    print("\n" + "=" * 60)
    print("TEST 4: Analytics Module")
    print("=" * 60)
    
    try:
        db = Database()
        db.connect()
        analytics = Analytics(db)
        
        # Get market activity
        print("Getting market activity...")
        activity = analytics.get_market_activity(days=30)
        
        if activity:
            print(f"✓ Found activity for {len(activity)} market(s)")
            db.disconnect()
            return True
        else:
            print("⚠ No market activity data (this is OK for new installation)")
            db.disconnect()
            return True
            
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_exporter():
    """Test export functionality"""
    print("\n" + "=" * 60)
    print("TEST 5: Export Module")
    print("=" * 60)
    
    try:
        db = Database()
        db.connect()
        analytics = Analytics(db)
        exporter = ReportExporter(analytics)
        
        # Check dependencies
        print("Checking export dependencies...")
        missing = exporter.check_dependencies()
        
        if not missing:
            print("✓ All export dependencies installed!")
            db.disconnect()
            return True
        else:
            print(f"⚠ Missing dependencies: {', '.join(missing)}")
            print("  Install with: pip install " + " ".join(missing))
            db.disconnect()
            return True  # Not a critical failure
            
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_permissions():
    """Test permissions module"""
    print("\n" + "=" * 60)
    print("TEST 6: Permissions Module")
    print("=" * 60)
    
    try:
        from src.permissions import Permissions
        from src.models import User
        
        # Create test users
        admin = User(1, 'admin', 'admin@test.com', 'hash', 'Admin', role='super_admin')
        seller = User(2, 'seller', 'seller@test.com', 'hash', 'Seller', role='seller')
        customer = User(3, 'customer', 'customer@test.com', 'hash', 'Customer', role='customer')
        
        print("Testing permission checks...")
        
        # Test admin permissions
        assert Permissions.is_super_admin(admin), "Admin check failed"
        assert Permissions.can_manage_users(admin), "Admin manage users failed"
        print("✓ Admin permissions working")
        
        # Test seller permissions
        assert Permissions.is_seller(seller), "Seller check failed"
        assert Permissions.can_manage_own_products(seller), "Seller manage products failed"
        print("✓ Seller permissions working")
        
        # Test customer permissions
        assert Permissions.is_customer(customer), "Customer check failed"
        assert Permissions.can_place_orders(customer), "Customer place orders failed"
        print("✓ Customer permissions working")
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("MARKET PRICE TRACKER - FEATURE TEST SUITE")
    print("=" * 60)
    print()
    
    tests = [
        ("Database Connection", test_connection),
        ("Authentication System", test_auth),
        ("User Management", test_user_manager),
        ("Analytics Module", test_analytics),
        ("Export Module", test_exporter),
        ("Permissions Module", test_permissions)
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ Test '{name}' crashed: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {name}")
    
    print(f"\n{passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your system is ready to use!")
        print("\nStart the application with:")
        print("  python main_enhanced.py")
        print("\nDefault login:")
        print("  Username: admin")
        print("  Password: admin123")
    else:
        print("\n⚠ Some tests failed. Please check the errors above.")
    
    print("=" * 60)


if __name__ == "__main__":
    main()
