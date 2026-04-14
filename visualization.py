import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import pandas as pd

class BMIVisualizer:
    """Creates BMI trend charts and statistics"""
    
    @staticmethod
    def create_trend_chart(history: list, user_id: str):
        """Create BMI trend line chart"""
        if not history:
            return
        
        df = pd.DataFrame(history)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        plt.figure(figsize=(12, 6))
        plt.plot(df['timestamp'], df['bmi'], marker='o', linewidth=2, markersize=6)
        plt.title(f'BMI Trend - {user_id}', fontsize=16, fontweight='bold')
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('BMI', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        
        # Add BMI category lines
        plt.axhline(y=18.5, color='green', linestyle='--', alpha=0.7, label='Normal (18.5)')
        plt.axhline(y=25.0, color='orange', linestyle='--', alpha=0.7, label='Overweight (25.0)')
        plt.axhline(y=30.0, color='red', linestyle='--', alpha=0.7, label='Obese (30.0)')
        plt.legend()
        
        plt.tight_layout()
        plt.savefig(f'bmi_trend_{user_id}.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    @staticmethod
    def create_category_pie_chart(history: list):
        """Create BMI category distribution pie chart"""
        if not history:
            return
        
        category_counts = pd.Series([record['category'] for record in history]).value_counts()
        
        plt.figure(figsize=(8, 8))
        colors = ['#FF6B6B', '#4ECDC4', '#FFE66D', '#FF8B94']
        wedges, texts, autotexts = plt.pie(category_counts.values, 
                                         labels=category_counts.index,
                                         autopct='%1.1f%%',
                                         colors=colors,
                                         startangle=90)
        
        plt.title('BMI Category Distribution', fontsize=16, fontweight='bold')
        plt.axis('equal')
        plt.tight_layout()
        plt.show()