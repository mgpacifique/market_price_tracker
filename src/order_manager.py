"""
Order management module
Handles order creation, tracking, and management
"""

from datetime import datetime
from src.models import Order, OrderItem


class OrderManager:
    """Manages order operations"""
    
    def __init__(self, database):
        """Initialize with database connection"""
        self.db = database
    
    def create_order(self, customer_id, market_id, items, delivery_address=None, 
                     delivery_phone=None, notes=None):
        """
        Create a new order with items
        items: list of dicts with keys: product_id, quantity, unit_price
        """
        # Calculate total
        total_amount = sum(item['quantity'] * item['unit_price'] for item in items)
        
        # Insert order
        order_query = """
        INSERT INTO orders (customer_id, market_id, total_amount, delivery_address, 
                           delivery_phone, notes, status)
        VALUES (%s, %s, %s, %s, %s, %s, 'pending')
        """
        
        success = self.db.execute_query(
            order_query,
            (customer_id, market_id, total_amount, delivery_address, delivery_phone, notes)
        )
        
        if not success:
            return False, None
        
        # Get the order_id of the newly created order
        order_id_query = "SELECT LAST_INSERT_ID() as order_id"
        result = self.db.execute_query(order_id_query, fetch=True)
        order_id = result[0]['order_id']
        
        # Insert order items
        item_query = """
        INSERT INTO order_items (order_id, product_id, quantity, unit_price, subtotal)
        VALUES (%s, %s, %s, %s, %s)
        """
        
        for item in items:
            subtotal = item['quantity'] * item['unit_price']
            self.db.execute_query(
                item_query,
                (order_id, item['product_id'], item['quantity'], item['unit_price'], subtotal)
            )
        
        return True, order_id
    
    def get_order_by_id(self, order_id):
        """Get order details by ID"""
        query = """
        SELECT o.*, u.full_name as customer_name, m.market_name
        FROM orders o
        JOIN users u ON o.customer_id = u.user_id
        JOIN markets m ON o.market_id = m.market_id
        WHERE o.order_id = %s
        """
        results = self.db.execute_query(query, (order_id,), fetch=True)
        
        if results:
            return Order(**results[0])
        return None
    
    def get_order_items(self, order_id):
        """Get all items for an order"""
        query = """
        SELECT oi.*, p.product_name, p.unit
        FROM order_items oi
        JOIN products p ON oi.product_id = p.product_id
        WHERE oi.order_id = %s
        """
        results = self.db.execute_query(query, (order_id,), fetch=True)
        
        if results:
            return [OrderItem(**row) for row in results]
        return []
    
    def get_customer_orders(self, customer_id, status=None):
        """Get all orders for a customer"""
        query = """
        SELECT o.*, m.market_name
        FROM orders o
        JOIN markets m ON o.market_id = m.market_id
        WHERE o.customer_id = %s
        """
        params = [customer_id]
        
        if status:
            query += " AND o.status = %s"
            params.append(status)
        
        query += " ORDER BY o.created_at DESC"
        
        results = self.db.execute_query(query, tuple(params), fetch=True)
        
        if results:
            return [Order(**row) for row in results]
        return []
    
    def get_market_orders(self, market_id, status=None):
        """Get all orders for a market (seller view)"""
        query = """
        SELECT o.*, u.full_name as customer_name
        FROM orders o
        JOIN users u ON o.customer_id = u.user_id
        WHERE o.market_id = %s
        """
        params = [market_id]
        
        if status:
            query += " AND o.status = %s"
            params.append(status)
        
        query += " ORDER BY o.created_at DESC"
        
        results = self.db.execute_query(query, tuple(params), fetch=True)
        
        if results:
            return [Order(**row) for row in results]
        return []
    
    def update_order_status(self, order_id, status):
        """Update order status"""
        valid_statuses = ['pending', 'confirmed', 'processing', 'ready', 'completed', 'cancelled']
        
        if status not in valid_statuses:
            return False, f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
        
        query = "UPDATE orders SET status = %s, updated_at = NOW() WHERE order_id = %s"
        success = self.db.execute_query(query, (status, order_id))
        
        if success:
            return True, f"Order status updated to {status}"
        return False, "Failed to update order status"
    
    def cancel_order(self, order_id, user_id, user_role):
        """Cancel an order (customer or admin only)"""
        # Get order details
        order = self.get_order_by_id(order_id)
        
        if not order:
            return False, "Order not found"
        
        # Check permissions
        if user_role != 'super_admin' and order.customer_id != user_id:
            return False, "You don't have permission to cancel this order"
        
        # Can only cancel if not yet completed
        if order.status in ['completed', 'cancelled']:
            return False, f"Cannot cancel order with status: {order.status}"
        
        return self.update_order_status(order_id, 'cancelled')
    
    def get_order_statistics(self, market_id=None, customer_id=None):
        """Get order statistics"""
        base_query = """
        SELECT 
            COUNT(*) as total_orders,
            SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) as pending_orders,
            SUM(CASE WHEN status = 'confirmed' THEN 1 ELSE 0 END) as confirmed_orders,
            SUM(CASE WHEN status = 'processing' THEN 1 ELSE 0 END) as processing_orders,
            SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed_orders,
            SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) as cancelled_orders,
            SUM(total_amount) as total_revenue,
            AVG(total_amount) as average_order_value
        FROM orders
        WHERE 1=1
        """
        
        params = []
        if market_id:
            base_query += " AND market_id = %s"
            params.append(market_id)
        
        if customer_id:
            base_query += " AND customer_id = %s"
            params.append(customer_id)
        
        results = self.db.execute_query(base_query, tuple(params), fetch=True)
        
        if results:
            return results[0]
        return None
