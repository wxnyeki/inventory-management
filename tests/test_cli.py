import pytest
from click.testing import CliRunner
from app.cli import cli

@pytest.fixture
def cli_runner():
    """Create a CLI test runner"""
    return CliRunner()

def test_cli_list_empty(cli_runner):
    """Test listing empty inventory"""
    result = cli_runner.invoke(cli, ['list'])
    assert result.exit_code == 0
    assert 'No items in inventory' in result.output

def test_cli_add_item(cli_runner):
    """Test adding an item via CLI"""
    result = cli_runner.invoke(cli, ['add'], input='Milk\n50\n3.99\n\n')
    assert result.exit_code == 0
    assert '✓ Item created' in result.output
    assert 'Milk' in result.output

def test_cli_list_items(cli_runner):
    """Test listing items"""
    # First add an item
    cli_runner.invoke(cli, ['add'], input='Milk\n50\n3.99\n\n')
    cli_runner.invoke(cli, ['add'], input='Cheese\n30\n5.99\n\n')
    
    # List items
    result = cli_runner.invoke(cli, ['list'])
    assert result.exit_code == 0
    assert 'Milk' in result.output
    assert 'Cheese' in result.output

def test_cli_search(cli_runner):
    """Test searching via CLI"""
    # Add items
    cli_runner.invoke(cli, ['add'], input='Milk\n50\n3.99\n\n')
    cli_runner.invoke(cli, ['add'], input='Cheese\n30\n5.99\n\n')
    
    # Search
    result = cli_runner.invoke(cli, ['search', 'Milk'])
    assert result.exit_code == 0
    assert 'Milk' in result.output
