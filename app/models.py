import json
import os
from datetime import datetime
from uuid import uuid4
from typing import List, Dict, Optional, Any

class InventoryItem:
    """Represents a single inventory item"""
    
    def __init__(self, name: str, quantity: int, price: float, barcode: str = None, id: str = None, created_at: str = None, updated_at: str = None):
        self.id = id or str(uuid4())
        self.name = name
        self.quantity = quantity
        self.price = price
        self.barcode = barcode
        self.created_at = created_at or datetime.now().isoformat()
        self.updated_at = updated_at or datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert item to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'quantity': self.quantity,
            'price': self.price,
            'barcode': self.barcode,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'InventoryItem':
        """Create item from dictionary"""
        return cls(
            name=data['name'],
            quantity=data['quantity'],
            price=data['price'],
            barcode=data.get('barcode'),
            id=data.get('id'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )
    
    def update(self, **kwargs) -> None:
        """Update item attributes"""
        for key, value in kwargs.items():
            if hasattr(self, key) and key not in ['id', 'created_at']:
                setattr(self, key, value)
        self.updated_at = datetime.now().isoformat()

class InventoryManager:
    """Manages inventory items with persistent JSON storage"""
    
    def __init__(self, json_file: str):
        self.json_file = json_file
        self._ensure_file_exists()
    
    def _ensure_file_exists(self) -> None:
        """Ensure the JSON file exists"""
        os.makedirs(os.path.dirname(self.json_file), exist_ok=True)
        if not os.path.exists(self.json_file):
            with open(self.json_file, 'w') as f:
                json.dump({'items': []}, f)
    
    def _load_data(self) -> Dict[str, List[Dict]]:
        """Load data from JSON file"""
        try:
            with open(self.json_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {'items': []}
    
    def _save_data(self, data: Dict[str, List[Dict]]) -> None:
        """Save data to JSON file"""
        with open(self.json_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def create_item(self, name: str, quantity: int, price: float, barcode: str = None) -> InventoryItem:
        """Create a new inventory item"""
        item = InventoryItem(name=name, quantity=quantity, price=price, barcode=barcode)
        data = self._load_data()
        data['items'].append(item.to_dict())
        self._save_data(data)
        return item
    
    def get_item(self, item_id: str) -> Optional[InventoryItem]:
        """Get item by ID"""
        data = self._load_data()
        for item_data in data['items']:
            if item_data['id'] == item_id:
                return InventoryItem.from_dict(item_data)
        return None
    
    def get_all_items(self) -> List[InventoryItem]:
        """Get all inventory items"""
        data = self._load_data()
        return [InventoryItem.from_dict(item_data) for item_data in data['items']]
    
    def update_item(self, item_id: str, **kwargs) -> Optional[InventoryItem]:
        """Update an inventory item"""
        data = self._load_data()
        for item_data in data['items']:
            if item_data['id'] == item_id:
                item = InventoryItem.from_dict(item_data)
                item.update(**kwargs)
                item_data.update(item.to_dict())
                self._save_data(data)
                return item
        return None
    
    def delete_item(self, item_id: str) -> bool:
        """Delete an inventory item"""
        data = self._load_data()
        original_length = len(data['items'])
        data['items'] = [item for item in data['items'] if item['id'] != item_id]
        if len(data['items']) < original_length:
            self._save_data(data)
            return True
        return False
    
    def get_item_by_barcode(self, barcode: str) -> Optional[InventoryItem]:
        """Get item by barcode"""
        data = self._load_data()
        for item_data in data['items']:
            if item_data.get('barcode') == barcode:
                return InventoryItem.from_dict(item_data)
        return None
    
    def search_items(self, query: str) -> List[InventoryItem]:
        """Search items by name"""
        data = self._load_data()
        query_lower = query.lower()
        return [
            InventoryItem.from_dict(item_data)
            for item_data in data['items']
            if query_lower in item_data['name'].lower()
        ]
