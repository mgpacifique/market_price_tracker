"""
Authentication module
Handles user registration, login, logout, and session management
"""

import bcrypt
import secrets
from datetime import datetime, timedelta
from src.models import User


class AuthManager:
    """Manages authentication operations"""
    
    def __init__(self, database):
        """Initialize with database connection"""
        self.db = database
        self.current_user = None
        self.current_session = None
    
    def hash_password(self, password):
        """Hash a password using bcrypt"""
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
        return password_hash.decode('utf-8')
    
    def verify_password(self, password, password_hash):
        """Verify a password against its hash"""
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
    
    def generate_session_token(self):
        """Generate a secure session token"""
        return secrets.token_urlsafe(32)
    
    def register_user(self, username, email, password, full_name, phone_number=None, role='customer'):
        """Register a new user"""
        # Check if username or email already exists
        check_query = "SELECT user_id FROM users WHERE username = %s OR email = %s"
        existing = self.db.execute_query(check_query, (username, email), fetch=True)
        
        if existing:
            return False, "Username or email already exists"
        
        # Hash password
        password_hash = self.hash_password(password)
        
        # Determine initial status based on role
        # Sellers need approval, customers are active immediately
        status = 'pending' if role == 'seller' else 'active'
        
        # Insert user
        query = """
        INSERT INTO users (username, email, password_hash, full_name, phone_number, role, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        success = self.db.execute_query(
            query, 
            (username, email, password_hash, full_name, phone_number, role, status)
        )
        
        if success:
            if role == 'seller':
                return True, "Registration successful! Your account is pending approval."
            return True, "Registration successful! You can now login."
        
        return False, "Registration failed. Please try again."
    
    def login(self, username_or_email, password):
        """Authenticate user and create session"""
        # Find user by username or email
        query = """
        SELECT * FROM users 
        WHERE (username = %s OR email = %s) 
        AND status != 'deleted'
        """
        results = self.db.execute_query(query, (username_or_email, username_or_email), fetch=True)
        
        if not results:
            return False, "Invalid username or password"
        
        user_data = results[0]
        
        # Check if account is active
        if user_data['status'] == 'suspended':
            return False, "Your account has been suspended. Please contact administrator."
        
        if user_data['status'] == 'pending':
            return False, "Your account is pending approval."
        
        # Verify password
        if not self.verify_password(password, user_data['password_hash']):
            return False, "Invalid username or password"
        
        # Create user object
        self.current_user = User(**user_data)
        
        # Create session
        session_token = self.generate_session_token()
        expires_at = datetime.now() + timedelta(days=7)
        
        session_query = """
        INSERT INTO user_sessions (user_id, session_token, expires_at)
        VALUES (%s, %s, %s)
        """
        self.db.execute_query(session_query, (self.current_user.user_id, session_token, expires_at))
        
        # Update last login
        update_query = "UPDATE users SET last_login = NOW() WHERE user_id = %s"
        self.db.execute_query(update_query, (self.current_user.user_id,))
        
        self.current_session = session_token
        
        return True, f"Welcome back, {self.current_user.full_name}!"
    
    def logout(self):
        """End current session"""
        if self.current_session:
            query = "DELETE FROM user_sessions WHERE session_token = %s"
            self.db.execute_query(query, (self.current_session,))
            self.current_session = None
            self.current_user = None
            return True
        return False
    
    def is_authenticated(self):
        """Check if user is currently authenticated"""
        return self.current_user is not None
    
    def get_current_user(self):
        """Get currently logged in user"""
        return self.current_user
    
    def has_role(self, role):
        """Check if current user has specific role"""
        if not self.current_user:
            return False
        return self.current_user.role == role
    
    def is_super_admin(self):
        """Check if current user is super admin"""
        return self.has_role('super_admin')
    
    def is_seller(self):
        """Check if current user is seller"""
        return self.has_role('seller')
    
    def is_customer(self):
        """Check if current user is customer"""
        return self.has_role('customer')
    
    def change_password(self, user_id, old_password, new_password):
        """Change user password"""
        # Get current password hash
        query = "SELECT password_hash FROM users WHERE user_id = %s"
        result = self.db.execute_query(query, (user_id,), fetch=True)
        
        if not result:
            return False, "User not found"
        
        # Verify old password
        if not self.verify_password(old_password, result[0]['password_hash']):
            return False, "Current password is incorrect"
        
        # Hash new password
        new_hash = self.hash_password(new_password)
        
        # Update password
        update_query = "UPDATE users SET password_hash = %s WHERE user_id = %s"
        success = self.db.execute_query(update_query, (new_hash, user_id))
        
        if success:
            return True, "Password changed successfully"
        return False, "Failed to change password"
    
    def clean_expired_sessions(self):
        """Remove expired sessions from database"""
        query = "DELETE FROM user_sessions WHERE expires_at < NOW()"
        return self.db.execute_query(query)
