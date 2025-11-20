"""
User management module
Handles user CRUD operations (super admin only)
"""

from src.models import User


class UserManager:
    """Manages user operations for super admin"""
    
    def __init__(self, database):
        """Initialize with database connection"""
        self.db = database
    
    def get_all_users(self, role=None, status=None):
        """Get all users with optional filters"""
        query = "SELECT * FROM users WHERE 1=1"
        params = []
        
        if role:
            query += " AND role = %s"
            params.append(role)
        
        if status:
            query += " AND status = %s"
            params.append(status)
        
        query += " ORDER BY created_at DESC"
        
        results = self.db.execute_query(query, tuple(params) if params else None, fetch=True)
        
        if results:
            return [User(**row) for row in results]
        return []
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        query = "SELECT * FROM users WHERE user_id = %s"
        results = self.db.execute_query(query, (user_id,), fetch=True)
        
        if results:
            return User(**results[0])
        return None
    
    def get_pending_sellers(self):
        """Get all pending seller registrations"""
        return self.get_all_users(role='seller', status='pending')
    
    def approve_seller(self, user_id):
        """Approve a pending seller account"""
        query = "UPDATE users SET status = 'active' WHERE user_id = %s AND role = 'seller'"
        success = self.db.execute_query(query, (user_id,))
        
        if success:
            return True, "Seller account approved"
        return False, "Failed to approve seller"
    
    def suspend_user(self, user_id, reason=None):
        """Suspend a user account"""
        query = "UPDATE users SET status = 'suspended' WHERE user_id = %s"
        success = self.db.execute_query(query, (user_id,))
        
        if success:
            # TODO: Add notification to user about suspension
            return True, "User account suspended"
        return False, "Failed to suspend user"
    
    def activate_user(self, user_id):
        """Activate a suspended user account"""
        query = "UPDATE users SET status = 'active' WHERE user_id = %s"
        success = self.db.execute_query(query, (user_id,))
        
        if success:
            return True, "User account activated"
        return False, "Failed to activate user"
    
    def delete_user(self, user_id):
        """Soft delete a user (mark as deleted)"""
        query = "UPDATE users SET status = 'deleted' WHERE user_id = %s"
        success = self.db.execute_query(query, (user_id,))
        
        if success:
            return True, "User deleted"
        return False, "Failed to delete user"
    
    def update_user_info(self, user_id, full_name=None, email=None, phone_number=None):
        """Update user information"""
        updates = []
        params = []
        
        if full_name:
            updates.append("full_name = %s")
            params.append(full_name)
        
        if email:
            updates.append("email = %s")
            params.append(email)
        
        if phone_number:
            updates.append("phone_number = %s")
            params.append(phone_number)
        
        if not updates:
            return False, "No updates provided"
        
        params.append(user_id)
        query = f"UPDATE users SET {', '.join(updates)} WHERE user_id = %s"
        
        success = self.db.execute_query(query, tuple(params))
        
        if success:
            return True, "User information updated"
        return False, "Failed to update user information"
    
    def get_user_statistics(self):
        """Get user statistics"""
        query = """
        SELECT 
            COUNT(*) as total_users,
            SUM(CASE WHEN role = 'super_admin' THEN 1 ELSE 0 END) as admins,
            SUM(CASE WHEN role = 'seller' THEN 1 ELSE 0 END) as sellers,
            SUM(CASE WHEN role = 'customer' THEN 1 ELSE 0 END) as customers,
            SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END) as active_users,
            SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) as pending_users,
            SUM(CASE WHEN status = 'suspended' THEN 1 ELSE 0 END) as suspended_users
        FROM users
        WHERE status != 'deleted'
        """
        
        results = self.db.execute_query(query, fetch=True)
        
        if results:
            return results[0]
        return None
    
    def search_users(self, search_term):
        """Search users by name, username, or email"""
        query = """
        SELECT * FROM users 
        WHERE (full_name LIKE %s OR username LIKE %s OR email LIKE %s)
        AND status != 'deleted'
        ORDER BY full_name
        """
        search_pattern = f"%{search_term}%"
        results = self.db.execute_query(
            query, 
            (search_pattern, search_pattern, search_pattern), 
            fetch=True
        )
        
        if results:
            return [User(**row) for row in results]
        return []
    
    def get_seller_market(self, user_id):
        """Get the market owned by a seller"""
        query = """
        SELECT * FROM markets 
        WHERE user_id = %s AND status = 'active'
        """
        results = self.db.execute_query(query, (user_id,), fetch=True)
        
        if results:
            from src.models import Market
            return Market(**results[0])
        return None
