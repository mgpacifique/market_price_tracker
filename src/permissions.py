"""
Permission and authorization module
Handles role-based access control (RBAC)
"""

from functools import wraps


class PermissionError(Exception):
    """Custom exception for permission errors"""
    pass


class Permissions:
    """Manages authorization and permissions"""
    
    # Permission levels
    SUPER_ADMIN = 'super_admin'
    SELLER = 'seller'
    CUSTOMER = 'customer'
    
    @staticmethod
    def require_auth(func):
        """Decorator to require authentication"""
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if not hasattr(self, 'auth') or not self.auth.is_authenticated():
                raise PermissionError("You must be logged in to perform this action")
            return func(self, *args, **kwargs)
        return wrapper
    
    @staticmethod
    def require_role(*allowed_roles):
        """Decorator to require specific role(s)"""
        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                if not hasattr(self, 'auth') or not self.auth.is_authenticated():
                    raise PermissionError("You must be logged in to perform this action")
                
                user = self.auth.get_current_user()
                if user.role not in allowed_roles:
                    raise PermissionError(f"This action requires one of the following roles: {', '.join(allowed_roles)}")
                
                return func(self, *args, **kwargs)
            return wrapper
        return decorator
    
    @staticmethod
    def is_super_admin(user):
        """Check if user is super admin"""
        return user and user.role == Permissions.SUPER_ADMIN
    
    @staticmethod
    def is_seller(user):
        """Check if user is seller"""
        return user and user.role == Permissions.SELLER
    
    @staticmethod
    def is_customer(user):
        """Check if user is customer"""
        return user and user.role == Permissions.CUSTOMER
    
    @staticmethod
    def can_manage_users(user):
        """Check if user can manage other users"""
        return Permissions.is_super_admin(user)
    
    @staticmethod
    def can_manage_all_products(user):
        """Check if user can manage all products"""
        return Permissions.is_super_admin(user)
    
    @staticmethod
    def can_manage_own_products(user):
        """Check if user can manage their own products"""
        return Permissions.is_super_admin(user) or Permissions.is_seller(user)
    
    @staticmethod
    def can_edit_product(user, product):
        """Check if user can edit a specific product"""
        if Permissions.is_super_admin(user):
            return True
        if Permissions.is_seller(user) and product.user_id == user.user_id:
            return True
        return False
    
    @staticmethod
    def can_manage_all_markets(user):
        """Check if user can manage all markets"""
        return Permissions.is_super_admin(user)
    
    @staticmethod
    def can_manage_own_market(user):
        """Check if user can manage their own market"""
        return Permissions.is_super_admin(user) or Permissions.is_seller(user)
    
    @staticmethod
    def can_edit_market(user, market):
        """Check if user can edit a specific market"""
        if Permissions.is_super_admin(user):
            return True
        if Permissions.is_seller(user) and market.user_id == user.user_id:
            return True
        return False
    
    @staticmethod
    def can_place_orders(user):
        """Check if user can place orders"""
        return Permissions.is_customer(user) or Permissions.is_super_admin(user)
    
    @staticmethod
    def can_view_order(user, order):
        """Check if user can view a specific order"""
        if Permissions.is_super_admin(user):
            return True
        if Permissions.is_customer(user) and order.customer_id == user.user_id:
            return True
        # Sellers can view orders for their market (need market check)
        if Permissions.is_seller(user):
            return True  # Will be validated with market ownership in the function
        return False
    
    @staticmethod
    def can_manage_order(user, order):
        """Check if user can manage (update status) a specific order"""
        if Permissions.is_super_admin(user):
            return True
        # Sellers can manage orders for their market
        if Permissions.is_seller(user):
            return True  # Will be validated with market ownership in the function
        return False
    
    @staticmethod
    def can_cancel_order(user, order):
        """Check if user can cancel a specific order"""
        if Permissions.is_super_admin(user):
            return True
        # Customers can cancel their own orders if not yet completed
        if Permissions.is_customer(user) and order.customer_id == user.user_id:
            if order.status not in ['completed', 'cancelled']:
                return True
        return False
    
    @staticmethod
    def can_view_analytics(user):
        """Check if user can view analytics"""
        return True  # All authenticated users can view analytics
    
    @staticmethod
    def can_export_reports(user):
        """Check if user can export reports"""
        return True  # All authenticated users can export reports
    
    @staticmethod
    def can_approve_sellers(user):
        """Check if user can approve seller accounts"""
        return Permissions.is_super_admin(user)
    
    @staticmethod
    def get_user_capabilities(user):
        """Get a list of capabilities for a user"""
        if not user:
            return []
        
        capabilities = []
        
        if Permissions.is_super_admin(user):
            capabilities = [
                'manage_users',
                'approve_sellers',
                'manage_all_products',
                'manage_all_markets',
                'view_all_orders',
                'manage_all_orders',
                'view_analytics',
                'export_reports',
                'system_admin'
            ]
        elif Permissions.is_seller(user):
            capabilities = [
                'manage_own_products',
                'manage_own_market',
                'view_own_orders',
                'manage_own_orders',
                'view_analytics',
                'export_reports'
            ]
        elif Permissions.is_customer(user):
            capabilities = [
                'browse_products',
                'place_orders',
                'view_own_orders',
                'cancel_own_orders',
                'view_analytics',
                'export_reports'
            ]
        
        return capabilities
