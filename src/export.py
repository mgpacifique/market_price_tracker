"""
Export and visualization module
Generates reports with charts and exports to PDF/Excel
"""

import os
from datetime import datetime
try:
    import matplotlib
    matplotlib.use('Agg')  # Use non-interactive backend
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


class ReportExporter:
    """Handles report generation and export"""
    
    def __init__(self, analytics):
        """Initialize with analytics instance"""
        self.analytics = analytics
        self.output_dir = 'reports'
        
        # Create reports directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def check_dependencies(self):
        """Check if required libraries are installed"""
        missing = []
        if not MATPLOTLIB_AVAILABLE:
            missing.append('matplotlib')
        if not PANDAS_AVAILABLE:
            missing.append('pandas')
        if not REPORTLAB_AVAILABLE:
            missing.append('reportlab')
        
        return missing
    
    def generate_price_trend_chart(self, product_id, product_name, market_id=None, 
                                   market_name=None, days=30):
        """Generate price trend line chart"""
        if not MATPLOTLIB_AVAILABLE:
            return None, "Matplotlib not installed"
        
        # Get trend data
        data = self.analytics.get_price_trend_data(product_id, market_id, days)
        
        if not data:
            return None, "No data available"
        
        # Prepare data
        dates = [datetime.strptime(str(d['date']), '%Y-%m-%d') for d in data]
        prices = [float(d['price']) for d in data]
        
        # Create plot
        plt.figure(figsize=(12, 6))
        plt.plot(dates, prices, marker='o', linestyle='-', linewidth=2, markersize=6)
        
        title = f"Price Trend: {product_name}"
        if market_name:
            title += f" at {market_name}"
        
        plt.title(title, fontsize=16, fontweight='bold')
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Price', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Save chart
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"price_trend_{product_id}_{timestamp}.png"
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filepath, "Chart generated successfully"
    
    def generate_market_comparison_chart(self, product_id, product_name):
        """Generate bar chart comparing prices across markets"""
        if not MATPLOTLIB_AVAILABLE:
            return None, "Matplotlib not installed"
        
        # Get comparison data
        data = self.analytics.get_market_price_comparison(product_id)
        
        if not data:
            return None, "No data available"
        
        # Prepare data
        markets = [d['market_name'] for d in data]
        prices = [float(d['price']) for d in data]
        
        # Create plot
        plt.figure(figsize=(12, 6))
        bars = plt.bar(markets, prices, color='steelblue', edgecolor='black', alpha=0.7)
        
        # Highlight min and max
        min_idx = prices.index(min(prices))
        max_idx = prices.index(max(prices))
        bars[min_idx].set_color('green')
        bars[max_idx].set_color('red')
        
        plt.title(f"Price Comparison Across Markets: {product_name}", 
                 fontsize=16, fontweight='bold')
        plt.xlabel('Market', fontsize=12)
        plt.ylabel('Price', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        
        # Save chart
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"market_comparison_{product_id}_{timestamp}.png"
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filepath, "Chart generated successfully"
    
    def export_to_excel(self, data, filename, sheet_name='Data'):
        """Export data to Excel file"""
        if not PANDAS_AVAILABLE:
            return None, "Pandas not installed. Cannot export to Excel."
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filepath = os.path.join(self.output_dir, f"{filename}_{timestamp}.xlsx")
        
        try:
            df = pd.DataFrame(data)
            df.to_excel(filepath, sheet_name=sheet_name, index=False)
            return filepath, "Excel file created successfully"
        except Exception as e:
            return None, f"Error creating Excel file: {str(e)}"
    
    def export_to_csv(self, data, filename):
        """Export data to CSV file"""
        if not PANDAS_AVAILABLE:
            return None, "Pandas not installed. Cannot export to CSV."
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filepath = os.path.join(self.output_dir, f"{filename}_{timestamp}.csv")
        
        try:
            df = pd.DataFrame(data)
            df.to_csv(filepath, index=False)
            return filepath, "CSV file created successfully"
        except Exception as e:
            return None, f"Error creating CSV file: {str(e)}"
    
    def generate_pdf_report(self, product_id, product_name, market_id=None, 
                           market_name=None, days=30):
        """Generate comprehensive PDF report with charts and statistics"""
        if not REPORTLAB_AVAILABLE:
            return None, "ReportLab not installed. Cannot generate PDF."
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"price_report_{product_id}_{timestamp}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            doc = SimpleDocTemplate(filepath, pagesize=letter)
            story = []
            styles = getSampleStyleSheet()
            
            # Title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#1f4788'),
                spaceAfter=30,
                alignment=1  # Center
            )
            
            title = Paragraph(f"Market Price Analysis Report<br/>{product_name}", title_style)
            story.append(title)
            story.append(Spacer(1, 12))
            
            # Report info
            info_text = f"""
            <b>Report Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br/>
            <b>Product:</b> {product_name}<br/>
            """
            if market_name:
                info_text += f"<b>Market:</b> {market_name}<br/>"
            info_text += f"<b>Analysis Period:</b> Last {days} days<br/>"
            
            story.append(Paragraph(info_text, styles['Normal']))
            story.append(Spacer(1, 20))
            
            # Get statistics
            stats = self.analytics.get_product_price_statistics(product_id, market_id, days)
            
            if stats:
                # Statistics section
                story.append(Paragraph("<b>Price Statistics</b>", styles['Heading2']))
                story.append(Spacer(1, 12))
                
                stats_data = [
                    ['Metric', 'Value'],
                    ['Minimum Price', f"{float(stats['min_price']):.2f}"],
                    ['Maximum Price', f"{float(stats['max_price']):.2f}"],
                    ['Average Price', f"{float(stats['avg_price']):.2f}"],
                    ['Standard Deviation', f"{float(stats['std_dev'] or 0):.2f}"],
                    ['Price Trend', stats['trend'].upper()],
                    ['Data Points', str(stats['data_points'])]
                ]
                
                stats_table = Table(stats_data, colWidths=[3*inch, 3*inch])
                stats_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 14),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                
                story.append(stats_table)
                story.append(Spacer(1, 20))
            
            # Generate and add charts
            if MATPLOTLIB_AVAILABLE:
                # Price trend chart
                chart_path, _ = self.generate_price_trend_chart(
                    product_id, product_name, market_id, market_name, days
                )
                if chart_path:
                    story.append(Paragraph("<b>Price Trend Over Time</b>", styles['Heading2']))
                    story.append(Spacer(1, 12))
                    img = Image(chart_path, width=6*inch, height=3*inch)
                    story.append(img)
                    story.append(Spacer(1, 20))
                
                # Market comparison chart (only if no specific market)
                if not market_id:
                    chart_path, _ = self.generate_market_comparison_chart(product_id, product_name)
                    if chart_path:
                        story.append(PageBreak())
                        story.append(Paragraph("<b>Market Price Comparison</b>", styles['Heading2']))
                        story.append(Spacer(1, 12))
                        img = Image(chart_path, width=6*inch, height=3*inch)
                        story.append(img)
            
            # Build PDF
            doc.build(story)
            return filepath, "PDF report generated successfully"
            
        except Exception as e:
            return None, f"Error generating PDF: {str(e)}"
    
    def generate_market_analytics_pdf(self, market_id, market_name, days=30):
        """Generate comprehensive market analytics PDF"""
        if not REPORTLAB_AVAILABLE:
            return None, "ReportLab not installed. Cannot generate PDF."
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"market_analytics_{market_id}_{timestamp}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            doc = SimpleDocTemplate(filepath, pagesize=letter)
            story = []
            styles = getSampleStyleSheet()
            
            # Title
            title = Paragraph(
                f"Market Analytics Report<br/>{market_name}",
                styles['Title']
            )
            story.append(title)
            story.append(Spacer(1, 20))
            
            # Get market report data
            report_data = self.analytics.generate_market_report(market_id, days)
            
            if report_data:
                # Market info
                story.append(Paragraph("<b>Market Information</b>", styles['Heading2']))
                story.append(Spacer(1, 12))
                
                info_text = f"""
                <b>Location:</b> {report_data['market_info']['location']}<br/>
                <b>Total Products:</b> {report_data['product_count']}<br/>
                <b>Analysis Period:</b> Last {days} days<br/>
                """
                story.append(Paragraph(info_text, styles['Normal']))
                story.append(Spacer(1, 20))
            
            doc.build(story)
            return filepath, "Market analytics PDF generated successfully"
            
        except Exception as e:
            return None, f"Error generating PDF: {str(e)}"
