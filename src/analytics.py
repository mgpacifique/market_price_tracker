"""
Analytics module
Handles price trend analysis, market comparisons, and statistics
"""

from datetime import datetime, timedelta
from collections import defaultdict


class Analytics:
    """Manages analytics and reporting operations"""
    
    def __init__(self, database):
        """Initialize with database connection"""
        self.db = database
    
    def get_price_trend_data(self, product_id, market_id=None, days=30):
        """
        Get price trend data for a product over time
        Returns list of {date, price, market_name} dicts
        """
        query = """
        SELECT p.date, p.price, m.market_name, m.market_id
        FROM prices p
        JOIN markets m ON p.market_id = m.market_id
        WHERE p.product_id = %s
        AND p.date >= DATE_SUB(CURDATE(), INTERVAL %s DAY)
        """
        params = [product_id, days]
        
        if market_id:
            query += " AND p.market_id = %s"
            params.append(market_id)
        
        query += " ORDER BY p.date ASC, m.market_name"
        
        results = self.db.execute_query(query, tuple(params), fetch=True)
        return results if results else []
    
    def get_market_price_comparison(self, product_id, date=None):
        """
        Compare latest prices of a product across all markets
        Returns list of {market_name, location, price, date} dicts
        """
        if date is None:
            # Get most recent prices
            query = """
            SELECT m.market_name, m.location, p.price, p.date
            FROM prices p
            JOIN markets m ON p.market_id = m.market_id
            WHERE p.product_id = %s
            AND p.date = (
                SELECT MAX(p2.date)
                FROM prices p2
                WHERE p2.product_id = p.product_id
                AND p2.market_id = p.market_id
            )
            ORDER BY p.price ASC
            """
            params = (product_id,)
        else:
            # Get prices for specific date
            query = """
            SELECT m.market_name, m.location, p.price, p.date
            FROM prices p
            JOIN markets m ON p.market_id = m.market_id
            WHERE p.product_id = %s AND p.date = %s
            ORDER BY p.price ASC
            """
            params = (product_id, date)
        
        results = self.db.execute_query(query, params, fetch=True)
        return results if results else []
    
    def get_product_price_statistics(self, product_id, market_id=None, days=30):
        """
        Get statistical analysis of product prices
        Returns dict with min, max, avg, median, std_dev, trend
        """
        query = """
        SELECT 
            MIN(price) as min_price,
            MAX(price) as max_price,
            AVG(price) as avg_price,
            COUNT(*) as data_points,
            STDDEV(price) as std_dev
        FROM prices
        WHERE product_id = %s
        AND date >= DATE_SUB(CURDATE(), INTERVAL %s DAY)
        """
        params = [product_id, days]
        
        if market_id:
            query += " AND market_id = %s"
            params.append(market_id)
        
        results = self.db.execute_query(query, tuple(params), fetch=True)
        
        if results and results[0]['data_points'] > 0:
            stats = results[0]
            
            # Calculate trend (comparing first half vs second half)
            trend = self._calculate_trend(product_id, market_id, days)
            stats['trend'] = trend
            
            return stats
        return None
    
    def _calculate_trend(self, product_id, market_id, days):
        """Calculate price trend direction"""
        query = """
        SELECT AVG(price) as avg_price, 
               CASE 
                   WHEN date >= DATE_SUB(CURDATE(), INTERVAL %s DAY) THEN 'recent'
                   ELSE 'older'
               END as period
        FROM prices
        WHERE product_id = %s
        AND date >= DATE_SUB(CURDATE(), INTERVAL %s DAY)
        """
        params = [days // 2, product_id, days]
        
        if market_id:
            query += " AND market_id = %s"
            params.append(market_id)
        
        query += " GROUP BY period"
        
        results = self.db.execute_query(query, tuple(params), fetch=True)
        
        if results and len(results) == 2:
            recent = next((r['avg_price'] for r in results if r['period'] == 'recent'), None)
            older = next((r['avg_price'] for r in results if r['period'] == 'older'), None)
            
            if recent and older:
                change_percent = ((float(recent) - float(older)) / float(older)) * 100
                
                if change_percent > 5:
                    return 'increasing'
                elif change_percent < -5:
                    return 'decreasing'
                else:
                    return 'stable'
        
        return 'unknown'
    
    def get_top_products_by_volume(self, limit=10):
        """Get most frequently priced products (indicates popularity)"""
        query = """
        SELECT 
            p.product_id,
            pr.product_name,
            pr.category,
            COUNT(*) as price_entries,
            AVG(p.price) as avg_price
        FROM prices p
        JOIN products pr ON p.product_id = pr.product_id
        WHERE p.date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
        GROUP BY p.product_id, pr.product_name, pr.category
        ORDER BY price_entries DESC
        LIMIT %s
        """
        
        results = self.db.execute_query(query, (limit,), fetch=True)
        return results if results else []
    
    def get_most_volatile_products(self, limit=10, days=30):
        """Get products with highest price volatility (standard deviation)"""
        query = """
        SELECT 
            p.product_id,
            pr.product_name,
            pr.category,
            pr.unit,
            MIN(p.price) as min_price,
            MAX(p.price) as max_price,
            AVG(p.price) as avg_price,
            STDDEV(p.price) as std_dev,
            (MAX(p.price) - MIN(p.price)) / AVG(p.price) * 100 as volatility_percent
        FROM prices p
        JOIN products pr ON p.product_id = pr.product_id
        WHERE p.date >= DATE_SUB(CURDATE(), INTERVAL %s DAY)
        GROUP BY p.product_id, pr.product_name, pr.category, pr.unit
        HAVING COUNT(*) >= 3
        ORDER BY volatility_percent DESC
        LIMIT %s
        """
        
        results = self.db.execute_query(query, (days, limit), fetch=True)
        return results if results else []
    
    def get_market_activity(self, days=30):
        """Get market activity statistics"""
        query = """
        SELECT 
            m.market_id,
            m.market_name,
            m.location,
            COUNT(DISTINCT p.product_id) as unique_products,
            COUNT(*) as total_price_entries,
            AVG(p.price) as avg_price
        FROM markets m
        JOIN prices p ON m.market_id = p.market_id
        WHERE p.date >= DATE_SUB(CURDATE(), INTERVAL %s DAY)
        GROUP BY m.market_id, m.market_name, m.location
        ORDER BY total_price_entries DESC
        """
        
        results = self.db.execute_query(query, (days,), fetch=True)
        return results if results else []
    
    def get_seasonal_patterns(self, product_id, months=12):
        """Analyze seasonal patterns in pricing"""
        query = """
        SELECT 
            MONTH(date) as month,
            YEAR(date) as year,
            AVG(price) as avg_price,
            MIN(price) as min_price,
            MAX(price) as max_price,
            COUNT(*) as data_points
        FROM prices
        WHERE product_id = %s
        AND date >= DATE_SUB(CURDATE(), INTERVAL %s MONTH)
        GROUP BY YEAR(date), MONTH(date)
        ORDER BY year, month
        """
        
        results = self.db.execute_query(query, (product_id, months), fetch=True)
        return results if results else []
    
    def get_price_forecast_data(self, product_id, market_id=None):
        """
        Get data for simple price forecasting
        Returns moving average and trend data
        """
        # Get last 60 days of data
        trend_data = self.get_price_trend_data(product_id, market_id, days=60)
        
        if not trend_data or len(trend_data) < 7:
            return None
        
        # Calculate 7-day moving average
        prices = [float(d['price']) for d in trend_data]
        moving_avg = []
        
        for i in range(len(prices)):
            if i < 6:
                moving_avg.append(sum(prices[:i+1]) / (i+1))
            else:
                moving_avg.append(sum(prices[i-6:i+1]) / 7)
        
        # Add moving average to data
        for i, item in enumerate(trend_data):
            item['moving_avg'] = moving_avg[i]
        
        return trend_data
    
    def generate_market_report(self, market_id, days=30):
        """Generate comprehensive market report"""
        # Market basic info
        market_query = "SELECT * FROM markets WHERE market_id = %s"
        market_info = self.db.execute_query(market_query, (market_id,), fetch=True)
        
        if not market_info:
            return None
        
        # Total products available
        products_query = """
        SELECT COUNT(DISTINCT product_id) as product_count
        FROM prices
        WHERE market_id = %s
        AND date >= DATE_SUB(CURDATE(), INTERVAL %s DAY)
        """
        product_count = self.db.execute_query(products_query, (market_id, days), fetch=True)
        
        # Price update frequency
        update_query = """
        SELECT COUNT(*) as total_updates,
               COUNT(*) / %s as avg_daily_updates
        FROM prices
        WHERE market_id = %s
        AND date >= DATE_SUB(CURDATE(), INTERVAL %s DAY)
        """
        update_stats = self.db.execute_query(update_query, (days, market_id, days), fetch=True)
        
        # Top products
        top_products_query = """
        SELECT p.product_name, pr.price, pr.date
        FROM prices pr
        JOIN products p ON pr.product_id = p.product_id
        WHERE pr.market_id = %s
        AND pr.date >= DATE_SUB(CURDATE(), INTERVAL %s DAY)
        ORDER BY pr.date DESC
        LIMIT 10
        """
        recent_prices = self.db.execute_query(top_products_query, (market_id, days), fetch=True)
        
        return {
            'market_info': market_info[0],
            'product_count': product_count[0]['product_count'] if product_count else 0,
            'update_stats': update_stats[0] if update_stats else {},
            'recent_prices': recent_prices if recent_prices else []
        }
