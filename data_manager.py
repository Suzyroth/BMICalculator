import json
import os
from datetime import datetime
from typing import List, Dict

class DataManager:
    """Manages user data storage and retrieval"""
    
    DATA_FILE = "bmi_data.json"
    
    def __init__(self):
        self.users_data = self.load_data()
    
    def load_data(self) -> Dict[str, List[Dict]]:
        """Load data from JSON file"""
        if os.path.exists(self.DATA_FILE):
            try:
                with open(self.DATA_FILE, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_data(self):
        """Save data to JSON file"""
        with open(self.DATA_FILE, 'w') as f:
            json.dump(self.users_data, f, indent=2)
    
    def add_record(self, user_id: str, weight: float, height: float, bmi: float, category: str):
        """Add new BMI record for user"""
        timestamp = datetime.now().isoformat()
        
        if user_id not in self.users_data:
            self.users_data[user_id] = []
        
        record = {
            'timestamp': timestamp,
            'weight': weight,
            'height': height,
            'bmi': round(bmi, 2),
            'category': category
        }
        
        self.users_data[user_id].append(record)
        self.save_data()
    
    def get_user_history(self, user_id: str) -> List[Dict]:
        """Get all records for a user"""
        return self.users_data.get(user_id, [])
    
    def get_all_users(self) -> List[str]:
        """Get list of all user IDs"""
        return list(self.users_data.keys())
    
    def delete_user_data(self, user_id: str):
        """Delete all data for a user"""
        if user_id in self.users_data:
            del self.users_data[user_id]
            self.save_data()