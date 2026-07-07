import pytest
import json
import os
from app import create_app
from app.models import InventoryManager, InventoryItem

@pytest.fixture
def app():
    """Create and configure a test app"""
    app = create_app('testing')
    yield app

@pytest.fixture
def client(app):
    """Create a test client"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Create a test CLI runner"""
    return app.test_cli_runner()

@pytest.fixture
def test_inventory_file(app):
    """Get test inventory file path"""
    return app.config['JSON_FILE']

@pytest.fixture
def inventory_manager(test_inventory_file):
    """Create an inventory manager for testing"""
    # Clean up test file before each test
    if os.path.exists(test_inventory_file):
        os.remove(test_inventory_file)
    return InventoryManager(test_inventory_file)

def cleanup_test_file(test_inventory_file):
    """Clean up test files"""
    if os.path.exists(test_inventory_file):
        os.remove(test_inventory_file)
