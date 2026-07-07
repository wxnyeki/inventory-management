import click
from app.models import InventoryManager
from config import Config
import os

class InventoryCLI:
    """Command-line interface for inventory management"""
    
    def __init__(self):
        self.manager = InventoryManager(Config.JSON_FILE)
    
    def add_item(self, name: str, quantity: int, price: float, barcode: str = None):
        """Add a new item"""
        item = self.manager.create_item(name, quantity, price, barcode)
        click.echo(f"✓ Item created: {item.name} (ID: {item.id})")
    
    def list_items(self):
        """List all items"""
        items = self.manager.get_all_items()
        if not items:
            click.echo("No items in inventory")
            return
        
        click.echo("\n" + "="*80)
        click.echo(f"{'ID':<36} {'Name':<20} {'Qty':>5} {'Price':>8} {'Barcode':<15}")
        click.echo("="*80)
        
        for item in items:
            click.echo(f"{item.id:<36} {item.name:<20} {item.quantity:>5} ${item.price:>7.2f} {item.barcode or '-':<15}")
        
        click.echo("="*80 + "\n")
    
    def get_item(self, item_id: str):
        """Get item details"""
        item = self.manager.get_item(item_id)
        if not item:
            click.echo(f"Item not found: {item_id}")
            return
        
        click.echo(f"\nItem Details:")
        click.echo(f"  ID: {item.id}")
        click.echo(f"  Name: {item.name}")
        click.echo(f"  Quantity: {item.quantity}")
        click.echo(f"  Price: ${item.price:.2f}")
        click.echo(f"  Barcode: {item.barcode or 'N/A'}")
        click.echo(f"  Created: {item.created_at}")
        click.echo(f"  Updated: {item.updated_at}\n")
    
    def update_item(self, item_id: str, **kwargs):
        """Update an item"""
        item = self.manager.update_item(item_id, **kwargs)
        if not item:
            click.echo(f"Item not found: {item_id}")
            return
        
        click.echo(f"✓ Item updated: {item.name}")
    
    def delete_item(self, item_id: str):
        """Delete an item"""
        success = self.manager.delete_item(item_id)
        if not success:
            click.echo(f"Item not found: {item_id}")
            return
        
        click.echo(f"✓ Item deleted: {item_id}")
    
    def search_items(self, query: str):
        """Search items"""
        items = self.manager.search_items(query)
        if not items:
            click.echo(f"No items found matching: {query}")
            return
        
        click.echo(f"\nSearch Results for '{query}':")
        click.echo("-" * 80)
        for item in items:
            click.echo(f"  {item.name} (ID: {item.id}) - Qty: {item.quantity}, Price: ${item.price:.2f}")
        click.echo("-" * 80 + "\n")

@click.group()
def cli():
    """Inventory Management CLI"""
    pass

@cli.command()
@click.option('--name', prompt='Item name', help='Name of the item')
@click.option('--quantity', prompt='Quantity', type=int, help='Quantity in stock')
@click.option('--price', prompt='Price', type=float, help='Price per unit')
@click.option('--barcode', default=None, help='Product barcode')
def add(name, quantity, price, barcode):
    """Add a new inventory item"""
    inventory_cli = InventoryCLI()
    inventory_cli.add_item(name, quantity, price, barcode)

@cli.command()
def list():
    """List all inventory items"""
    inventory_cli = InventoryCLI()
    inventory_cli.list_items()

@cli.command()
@click.argument('item_id')
def get(item_id):
    """Get details of a specific item"""
    inventory_cli = InventoryCLI()
    inventory_cli.get_item(item_id)

@cli.command()
@click.argument('item_id')
@click.option('--name', default=None, help='New name')
@click.option('--quantity', default=None, type=int, help='New quantity')
@click.option('--price', default=None, type=float, help='New price')
def update(item_id, name, quantity, price):
    """Update an inventory item"""
    inventory_cli = InventoryCLI()
    updates = {}
    if name:
        updates['name'] = name
    if quantity is not None:
        updates['quantity'] = quantity
    if price is not None:
        updates['price'] = price
    
    if not updates:
        click.echo("No updates provided")
        return
    
    inventory_cli.update_item(item_id, **updates)

@cli.command()
@click.argument('item_id')
def delete(item_id):
    """Delete an inventory item"""
    inventory_cli = InventoryCLI()
    if click.confirm(f"Are you sure you want to delete item {item_id}?"):
        inventory_cli.delete_item(item_id)

@cli.command()
@click.argument('query')
def search(query):
    """Search inventory items"""
    inventory_cli = InventoryCLI()
    inventory_cli.search_items(query)

if __name__ == '__main__':
    cli()
