import json
import os
from typing import Dict, Optional

class CustomCategoryManager:
    def __init__(self):
        self.file_path = 'data/custom_categories.json'
        self._ensure_file_exists()
        
    def _ensure_file_exists(self):
        if not os.path.exists('data'):
            os.makedirs('data')
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump({}, f)
    
    def get_custom_categories(self) -> Dict:
        with open(self.file_path, 'r') as f:
            return json.load(f)
    
    def add_custom_category(self, name: str, icon: str, color: str) -> None:
        categories = self.get_custom_categories()
        categories[name] = {
            'icon': icon,
            'color': color
        }
        with open(self.file_path, 'w') as f:
            json.dump(categories, f, indent=2)
    
    def get_category(self, name: str) -> Optional[Dict]:
        categories = self.get_custom_categories()
        return categories.get(name)
