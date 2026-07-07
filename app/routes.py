from flask import Blueprint, request, jsonify
from app.models import InventoryManager
from app.external_api import OpenFoodFactsAPI, ExternalAPIService
import os

# Create blueprint
bp = Blueprint('api', __name__, url_prefix='/api')

# Initialize managers
inventory_manager = None
api_service = None

def init_routes(app):
    """Initialize routes with app instance"""
    global inventory_manager, api_service
    
    from config import config
    env = os.getenv('FLASK_ENV', 'development')
    cfg = config.get(env, config['default'])
    
    inventory_manager = InventoryManager(cfg.JSON_FILE)
    
    openfacts_api = OpenFoodFactsAPI(
        base_url=cfg.OPENFOODFACTS_API_URL,
        search_url=cfg.OPENFOODFACTS_SEARCH_URL,
        timeout=cfg.REQUEST_TIMEOUT
    )
    api_service = ExternalAPIService(openfacts_api)
    
    app.register_blueprint(bp)

# ==================== INVENTORY ROUTES ====================

@bp.route('/inventory', methods=['GET'])
def get_inventory():
    """Get all inventory items"""
    try:
        items = inventory_manager.get_all_items()
        return jsonify({
            'status': 'success',
            'count': len(items),
            'items': [item.to_dict() for item in items]
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@bp.route('/inventory/<item_id>', methods=['GET'])
def get_item(item_id):
    """Get a specific inventory item"""
    try:
        item = inventory_manager.get_item(item_id)
        if not item:
            return jsonify({'status': 'error', 'message': 'Item not found'}), 404
        return jsonify({
            'status': 'success',
            'item': item.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@bp.route('/inventory', methods=['POST'])
def create_item():
    """Create a new inventory item"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'name' not in data or 'quantity' not in data or 'price' not in data:
            return jsonify({'status': 'error', 'message': 'Missing required fields: name, quantity, price'}), 400
        
        item = inventory_manager.create_item(
            name=data['name'],
            quantity=int(data['quantity']),
            price=float(data['price']),
            barcode=data.get('barcode')
        )
        
        return jsonify({
            'status': 'success',
            'message': 'Item created successfully',
            'item': item.to_dict()
        }), 201
    except ValueError as e:
        return jsonify({'status': 'error', 'message': f'Invalid data type: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@bp.route('/inventory/<item_id>', methods=['PUT'])
def update_item(item_id):
    """Update an inventory item"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'status': 'error', 'message': 'No data provided'}), 400
        
        item = inventory_manager.update_item(item_id, **data)
        
        if not item:
            return jsonify({'status': 'error', 'message': 'Item not found'}), 404
        
        return jsonify({
            'status': 'success',
            'message': 'Item updated successfully',
            'item': item.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@bp.route('/inventory/<item_id>', methods=['DELETE'])
def delete_item(item_id):
    """Delete an inventory item"""
    try:
        success = inventory_manager.delete_item(item_id)
        
        if not success:
            return jsonify({'status': 'error', 'message': 'Item not found'}), 404
        
        return jsonify({
            'status': 'success',
            'message': 'Item deleted successfully'
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# ==================== SEARCH ROUTES ====================

@bp.route('/search', methods=['GET'])
def search_items():
    """Search inventory items by name"""
    try:
        query = request.args.get('q', '').strip()
        
        if not query:
            return jsonify({'status': 'error', 'message': 'Search query required'}), 400
        
        items = inventory_manager.search_items(query)
        
        return jsonify({
            'status': 'success',
            'count': len(items),
            'query': query,
            'items': [item.to_dict() for item in items]
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@bp.route('/search/barcode', methods=['POST'])
def search_by_barcode():
    """Search external API by barcode"""
    try:
        data = request.get_json()
        
        if not data or 'barcode' not in data:
            return jsonify({'status': 'error', 'message': 'Barcode required'}), 400
        
        product = api_service.import_product_by_barcode(data['barcode'])
        
        if not product:
            return jsonify({'status': 'error', 'message': 'Product not found'}), 404
        
        # Check if product already in inventory
        existing = inventory_manager.get_item_by_barcode(data['barcode'])
        
        return jsonify({
            'status': 'success',
            'product': product,
            'in_inventory': existing is not None
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@bp.route('/search/name', methods=['POST'])
def search_by_name():
    """Search external API by product name"""
    try:
        data = request.get_json()
        
        if not data or 'name' not in data:
            return jsonify({'status': 'error', 'message': 'Product name required'}), 400
        
        products = api_service.import_product_by_name(data['name'])
        
        if not products:
            return jsonify({'status': 'error', 'message': 'No products found'}), 404
        
        return jsonify({
            'status': 'success',
            'count': len(products),
            'products': products
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@bp.route('/import', methods=['POST'])
def import_product():
    """Import product from external API and add to inventory"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'status': 'error', 'message': 'No data provided'}), 400
        
        # Create item with provided data
        item = inventory_manager.create_item(
            name=data.get('name', 'Unknown Product'),
            quantity=int(data.get('quantity', 0)),
            price=float(data.get('price', 0)),
            barcode=data.get('barcode')
        )
        
        return jsonify({
            'status': 'success',
            'message': 'Product imported successfully',
            'item': item.to_dict()
        }), 201
    except ValueError as e:
        return jsonify({'status': 'error', 'message': f'Invalid data type: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# ==================== HEALTH CHECK ====================

@bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'}), 200
