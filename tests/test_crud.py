import pytest
from app.models import InventoryItem, InventoryManager
import os

def test_inventory_item_creation():
    """Test creating an inventory item"""
    item = InventoryItem(name="Milk", quantity=50, price=3.99, barcode="123456789")
    assert item.name == "Milk"
    assert item.quantity == 50
    assert item.price == 3.99
    assert item.barcode == "123456789"
    assert item.id is not None

def test_inventory_item_to_dict():
    """Test converting item to dictionary"""
    item = InventoryItem(name="Bread", quantity=20, price=2.50)
    item_dict = item.to_dict()
    assert item_dict['name'] == "Bread"
    assert item_dict['quantity'] == 20
    assert item_dict['price'] == 2.50
    assert 'id' in item_dict
    assert 'created_at' in item_dict
    assert 'updated_at' in item_dict

def test_inventory_item_from_dict():
    """Test creating item from dictionary"""
    data = {
        'id': '123',
        'name': 'Cheese',
        'quantity': 15,
        'price': 5.99,
        'barcode': '987654321',
        'created_at': '2024-01-01T00:00:00',
        'updated_at': '2024-01-01T00:00:00'
    }
    item = InventoryItem.from_dict(data)
    assert item.id == '123'
    assert item.name == 'Cheese'
    assert item.quantity == 15
    assert item.price == 5.99

def test_inventory_item_update():
    """Test updating an item"""
    item = InventoryItem(name="Butter", quantity=10, price=4.99)
    original_id = item.id
    original_created = item.created_at
    
    item.update(quantity=20, price=5.99)
    
    assert item.quantity == 20
    assert item.price == 5.99
    assert item.id == original_id
    assert item.created_at == original_created

def test_inventory_manager_create(inventory_manager):
    """Test creating an item in the manager"""
    item = inventory_manager.create_item("Eggs", 100, 2.99)
    assert item.name == "Eggs"
    assert item.quantity == 100
    assert item.price == 2.99

def test_inventory_manager_get(inventory_manager):
    """Test getting an item from the manager"""
    created = inventory_manager.create_item("Milk", 50, 3.99)
    retrieved = inventory_manager.get_item(created.id)
    assert retrieved is not None
    assert retrieved.name == "Milk"
    assert retrieved.id == created.id

def test_inventory_manager_get_nonexistent(inventory_manager):
    """Test getting a nonexistent item"""
    result = inventory_manager.get_item("nonexistent-id")
    assert result is None

def test_inventory_manager_get_all(inventory_manager):
    """Test getting all items"""
    inventory_manager.create_item("Item1", 10, 1.00)
    inventory_manager.create_item("Item2", 20, 2.00)
    inventory_manager.create_item("Item3", 30, 3.00)
    
    items = inventory_manager.get_all_items()
    assert len(items) == 3

def test_inventory_manager_update(inventory_manager):
    """Test updating an item"""
    created = inventory_manager.create_item("Item", 10, 5.00)
    updated = inventory_manager.update_item(created.id, quantity=20, price=6.00)
    
    assert updated is not None
    assert updated.quantity == 20
    assert updated.price == 6.00

def test_inventory_manager_delete(inventory_manager):
    """Test deleting an item"""
    created = inventory_manager.create_item("Item", 10, 5.00)
    success = inventory_manager.delete_item(created.id)
    
    assert success is True
    assert inventory_manager.get_item(created.id) is None

def test_inventory_manager_delete_nonexistent(inventory_manager):
    """Test deleting a nonexistent item"""
    success = inventory_manager.delete_item("nonexistent-id")
    assert success is False

def test_inventory_manager_get_by_barcode(inventory_manager):
    """Test getting item by barcode"""
    created = inventory_manager.create_item("Milk", 50, 3.99, barcode="123456789")
    retrieved = inventory_manager.get_item_by_barcode("123456789")
    
    assert retrieved is not None
    assert retrieved.id == created.id

def test_inventory_manager_search(inventory_manager):
    """Test searching items by name"""
    inventory_manager.create_item("Milk", 50, 3.99)
    inventory_manager.create_item("Cheese", 30, 5.99)
    inventory_manager.create_item("Butter", 40, 4.99)
    
    results = inventory_manager.search_items("milk")
    assert len(results) == 1
    assert results[0].name == "Milk"
    
    results = inventory_manager.search_items("Da")  # no match
    assert len(results) == 0
