import pytest
from unittest.mock import patch, MagicMock
from app.external_api import OpenFoodFactsAPI, ExternalAPIService

@pytest.fixture
def api():
    """Create OpenFoodFacts API instance"""
    return OpenFoodFactsAPI(
        base_url='https://world.openfoodfacts.org/api/v0/product',
        search_url='https://world.openfoodfacts.org/cgi/search.pl'
    )

def test_search_by_barcode_success(api):
    """Test successful barcode search"""
    mock_response = {
        'status': 1,
        'product': {
            'product_name': 'Organic Milk',
            'brands': 'LocalFarm',
            'quantity': '1L',
            'categories': 'Dairy',
            'nutrition_grade_fr': 'A',
            'nutriments': {
                'energy-kcal_100g': 61,
                'fat_100g': 3.5,
                'carbohydrates_100g': 4.8,
                'proteins_100g': 3.2
            }
        }
    }
    
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = mock_response
        result = api.search_by_barcode('5000112599682')
        
        assert result is not None
        assert result['name'] == 'Organic Milk'
        assert result['brand'] == 'LocalFarm'
        assert result['nutrition_grade'] == 'A'

def test_search_by_barcode_not_found(api):
    """Test barcode not found"""
    mock_response = {'status': 0}
    
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = mock_response
        result = api.search_by_barcode('9999999999999')
        
        assert result is None

def test_search_by_barcode_error(api):
    """Test barcode search error"""
    with patch('requests.get') as mock_get:
        mock_get.side_effect = Exception("Network error")
        result = api.search_by_barcode('5000112599682')
        
        assert result is None

def test_search_by_name_success(api):
    """Test successful name search"""
    mock_response = {
        'products': [
            {
                'product_name': 'Milk 1L',
                'code': '123456789',
                'brands': 'Brand A',
                'quantity': '1L',
                'categories': 'Dairy',
                'nutrition_grade_fr': 'A'
            },
            {
                'product_name': 'Milk 2L',
                'code': '987654321',
                'brands': 'Brand B',
                'quantity': '2L',
                'categories': 'Dairy',
                'nutrition_grade_fr': 'B'
            }
        ]
    }
    
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = mock_response
        result = api.search_by_name('milk')
        
        assert result is not None
        assert len(result) == 2
        assert result[0]['name'] == 'Milk 1L'

def test_search_by_name_not_found(api):
    """Test name search not found"""
    mock_response = {'products': []}
    
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = mock_response
        result = api.search_by_name('unknown-product')
        
        assert result is None

def test_external_api_service(api):
    """Test ExternalAPIService"""
    service = ExternalAPIService(api)
    assert service.api == api

def test_external_api_service_import_by_barcode(api):
    """Test importing product by barcode via service"""
    mock_response = {
        'status': 1,
        'product': {
            'product_name': 'Test Product',
            'brands': 'Test Brand',
            'quantity': '1L',
            'categories': 'Test',
            'nutrition_grade_fr': 'A',
            'nutriments': {}
        }
    }
    
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = mock_response
        service = ExternalAPIService(api)
        result = service.import_product_by_barcode('123456')
        
        assert result is not None
        assert result['name'] == 'Test Product'
