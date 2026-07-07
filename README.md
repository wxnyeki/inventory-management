# Inventory Management System

A Flask-based REST API with an administrator portal for managing e-commerce inventory. This system integrates with the OpenFoodFacts API to fetch real-time product data and includes a CLI interface for managing inventory items.

## Features

- **CRUD Operations**: Create, read, update, and delete inventory items
- **External API Integration**: Fetch product details from OpenFoodFacts API by barcode or name
- **REST API**: Flask-based REST API endpoints
- **CLI Interface**: Command-line interface for inventory management
- **Unit Tests**: Comprehensive test suite for all functionality
- **Data Persistence**: JSON-based storage for inventory data

## Project Structure

```
inventory-management/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── models.py
│   ├── external_api.py
│   └── cli.py
├── tests/
│   ���── __init__.py
│   ├── test_routes.py
│   ├── test_crud.py
│   ├── test_external_api.py
│   └── test_cli.py
├── data/
│   └── inventory.json
├── requirements.txt
├── config.py
├── run.py
└── README.md
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/wxnyeki/inventory-management.git
   cd inventory-management
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the API Server

```bash
python run.py
```

The API will be available at `http://localhost:5000`

### Using the CLI Interface

```bash
python -m app.cli
```

## API Endpoints

### Inventory Management

- `GET /api/inventory` - Retrieve all inventory items
- `GET /api/inventory/<id>` - Retrieve a specific item
- `POST /api/inventory` - Create a new inventory item
- `PUT /api/inventory/<id>` - Update an inventory item
- `DELETE /api/inventory/<id>` - Delete an inventory item

### External API Integration

- `POST /api/search/barcode` - Search product by barcode
- `POST /api/search/name` - Search product by name
- `POST /api/import` - Import product data and add to inventory

## API Request Examples

### Create an Inventory Item

```bash
curl -X POST http://localhost:5000/api/inventory \
  -H "Content-Type: application/json" \
  -d '{"name": "Milk", "quantity": 50, "price": 3.99, "barcode": "123456789"}'
```

### Search External API by Barcode

```bash
curl -X POST http://localhost:5000/api/search/barcode \
  -H "Content-Type: application/json" \
  -d '{"barcode": "5000112599682"}'
```

### Get All Inventory Items

```bash
curl http://localhost:5000/api/inventory
```

## Testing

Run the test suite:

```bash
python -m pytest tests/ -v
```

Run tests with coverage:

```bash
python -m pytest tests/ --cov=app --cov-report=html
```

## Testing Coverage

- **Route Testing**: Validates all Flask routes and HTTP methods
- **CRUD Operations**: Tests create, read, update, and delete functionality
- **External API Integration**: Tests API calls to OpenFoodFacts
- **CLI Interface**: Tests command-line functionality
- **Error Handling**: Tests error responses and edge cases

## Configuration

Edit `config.py` to customize settings:

```python
DEBUG = True
TESTING = False
JSON_FILE = 'data/inventory.json'
OPENFOODFACTS_API_URL = 'https://world.openfoodfacts.org/api/v0/product'
```

## External API: OpenFoodFacts

This system integrates with the [OpenFoodFacts API](https://world.openfoodfacts.org/api) to fetch product details. The API allows:

- **Barcode Search**: Retrieve product information using an 8 or 13-digit barcode
- **Product Name Search**: Search for products by name

### API Example

```bash
# Search by barcode
curl "https://world.openfoodfacts.org/api/v0/product/5000112599682.json"

# Search by name
curl "https://world.openfoodfacts.org/cgi/search.pl?action=process&search_terms=milk&json=1"
```

## Git Workflow

This project uses feature branches for development:

1. `feature/project-setup` - Initial project structure
2. `feature/flask-api` - Flask REST API with CRUD operations
3. `feature/external-api` - External API integration
4. `feature/cli-interface` - CLI interface
5. `feature/testing` - Unit tests and test suite

Each feature is developed on its own branch and merged to `main` via pull requests.

## Development Process

### Task 1: Define the Problem ✓
- Inventory management system requirements
- CRUD operations needed
- External API integration requirements

### Task 2: Determine the Design ✓
- Flask REST API architecture
- JSON-based data storage
- CLI interface design
- Test strategy

### Task 3: Develop the Code
- Flask routes and endpoints
- CRUD operations implementation
- External API integration
- CLI interface development

### Task 4: Test and Debug
- Unit tests for all features
- Integration tests
- Manual testing and debugging

### Task 5: Document and Maintain
- API documentation
- Code comments and docstrings
- README and setup instructions
- Maintenance guidelines

## Requirements

- Python 3.8+
- Flask
- Requests
- Pytest
- Pytest-cov

## License

MIT License

## Author

wxnyeki
