import requests
from typing import Dict, Optional, Any
import logging

logger = logging.getLogger(__name__)

class OpenFoodFactsAPI:
    """Integration with OpenFoodFacts API for product lookup"""
    
    def __init__(self, base_url: str, search_url: str, timeout: int = 10):
        self.base_url = base_url
        self.search_url = search_url
        self.timeout = timeout
    
    def search_by_barcode(self, barcode: str) -> Optional[Dict[str, Any]]:
        """
        Search for product by barcode
        
        Args:
            barcode: Product barcode (8 or 13 digits)
        
        Returns:
            Product data dictionary or None if not found
        """
        try:
            url = f"{self.base_url}/{barcode}.json"
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            if data.get('status') == 1 and 'product' in data:
                product = data['product']
                return {
                    'name': product.get('product_name', 'Unknown'),
                    'barcode': barcode,
                    'brand': product.get('brands', ''),
                    'quantity': product.get('quantity', ''),
                    'categories': product.get('categories', ''),
                    'nutrition_grade': product.get('nutrition_grade_fr', ''),
                    'energy_kcal': product.get('nutriments', {}).get('energy-kcal_100g'),
                    'fat': product.get('nutriments', {}).get('fat_100g'),
                    'carbohydrates': product.get('nutriments', {}).get('carbohydrates_100g'),
                    'proteins': product.get('nutriments', {}).get('proteins_100g'),
                }
            return None
        except requests.RequestException as e:
            logger.error(f"Error searching barcode {barcode}: {str(e)}")
            return None
    
    def search_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Search for products by name
        
        Args:
            name: Product name
        
        Returns:
            List of matching products or None if error
        """
        try:
            params = {
                'action': 'process',
                'search_terms': name,
                'json': 1
            }
            response = requests.get(self.search_url, params=params, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            products = []
            
            if 'products' in data:
                for product in data['products'][:5]:  # Limit to 5 results
                    products.append({
                        'name': product.get('product_name', 'Unknown'),
                        'barcode': product.get('code', ''),
                        'brand': product.get('brands', ''),
                        'quantity': product.get('quantity', ''),
                        'categories': product.get('categories', ''),
                        'nutrition_grade': product.get('nutrition_grade_fr', ''),
                    })
            
            return products if products else None
        except requests.RequestException as e:
            logger.error(f"Error searching name {name}: {str(e)}")
            return None

class ExternalAPIService:
    """Service for managing external API calls"""
    
    def __init__(self, api_instance: OpenFoodFactsAPI):
        self.api = api_instance
    
    def import_product_by_barcode(self, barcode: str) -> Optional[Dict[str, Any]]:
        """Import product data by barcode"""
        return self.api.search_by_barcode(barcode)
    
    def import_product_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Import product data by name"""
        return self.api.search_by_name(name)
