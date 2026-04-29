import pytest
from unittest.mock import MagicMock
from django_app.core.services.product_service import ProductService
from django_app.core.models.product import Product

# ─── Helpers ────────────────────────────────────────────────

def make_product(**kwargs):
    """Helper to create a Product with sensible defaults"""
    defaults = dict(
        id="507f1e77bcf86cd799439011",
        name="Test Keyboard",
        description="A test product",
        price=4999.0,
        brand="Keychron",
        quantity=50,
        category=None,
        category_id=None,
    )
    defaults.update(kwargs)
    return Product(**defaults)


def make_service(saved_product=None, found_product=None, category_found=True):
    """Helper to build a ProductService with mocked repositories"""
    mock_repo = MagicMock()
    mock_category_repo = MagicMock()

    # Default behaviours
    mock_repo.save.return_value = saved_product or make_product()
    mock_repo.find_by_id.return_value = found_product
    mock_repo.find_all.return_value = []
    mock_repo.delete.return_value = True

    mock_category_repo.find_by_id.return_value = (
        MagicMock() if category_found else None
    )

    service = ProductService(
        repository=mock_repo,
        category_repository=mock_category_repo
    )
    return service, mock_repo, mock_category_repo


# ─── create_product ─────────────────────────────────────────

class TestCreateProduct:

    def test_creates_product_with_valid_data(self):
        service, mock_repo, _ = make_service()
        data = {
            "name": "Keyboard",
            "price": 4999.0,
            "brand": "Keychron",
            "quantity": 10,
            "description": "Clicky",
        }
        result = service.create_product(data)

        mock_repo.save.assert_called_once()   # repo.save was called
        assert result.name == "Test Keyboard"  # returns what repo.save returns

    def test_raises_when_name_missing(self):
        service, _, _ = make_service()
        with pytest.raises(ValueError) as exc_info:
            service.create_product({
                "price": 4999.0,
                "brand": "Keychron",
                "quantity": 10
            })
        assert "name" in exc_info.value.args[0]

    def test_raises_when_brand_missing(self):
        service, _, _ = make_service()
        with pytest.raises(ValueError) as exc_info:
            service.create_product({
                "name": "Keyboard",
                "price": 4999.0,
                "quantity": 10
            })
        assert "brand" in exc_info.value.args[0]

    def test_raises_when_price_is_zero(self):
        service, _, _ = make_service()
        with pytest.raises(ValueError) as exc_info:
            service.create_product({
                "name": "Keyboard",
                "brand": "Keychron",
                "price": 0,
                "quantity": 10
            })
        assert "price" in exc_info.value.args[0]

    def test_raises_when_price_is_negative(self):
        service, _, _ = make_service()
        with pytest.raises(ValueError) as exc_info:
            service.create_product({
                "name": "Keyboard",
                "brand": "Keychron",
                "price": -100,
                "quantity": 10
            })
        assert "price" in exc_info.value.args[0]

    def test_raises_when_quantity_is_negative(self):
        service, _, _ = make_service()
        with pytest.raises(ValueError) as exc_info:
            service.create_product({
                "name": "Keyboard",
                "brand": "Keychron",
                "price": 4999.0,
                "quantity": -1
            })
        assert "quantity" in exc_info.value.args[0]

    def test_raises_when_category_not_found(self):
        service, _, _ = make_service(category_found=False)
        with pytest.raises(ValueError) as exc_info:
            service.create_product({
                "name": "Keyboard",
                "brand": "Keychron",
                "price": 4999.0,
                "quantity": 10,
                "category_id": "nonexistent_id"
            })
        assert "category_id" in exc_info.value.args[0]

    def test_multiple_validation_errors_returned_together(self):
        """All errors should be returned at once, not one at a time"""
        service, _, _ = make_service()
        with pytest.raises(ValueError) as exc_info:
            service.create_product({
                "price": -100,
                "quantity": -5
                # name and brand also missing
            })
        errors = exc_info.value.args[0]
        assert "name" in errors
        assert "brand" in errors
        assert "price" in errors
        assert "quantity" in errors


# ─── get_product ─────────────────────────────────────────────

class TestGetProduct:

    def test_returns_product_when_found(self):
        product = make_product(name="Found Product")
        service, mock_repo, _ = make_service(found_product=product)

        result = service.get_product("507f1e77bcf86cd799439011")

        mock_repo.find_by_id.assert_called_once_with("507f1e77bcf86cd799439011")
        assert result.name == "Found Product"

    def test_returns_none_when_not_found(self):
        service, _, _ = make_service(found_product=None)
        result = service.get_product("nonexistent")
        assert result is None


# ─── update_product ───────────────────────────────────────────

class TestUpdateProduct:

    def test_updates_product_when_exists(self):
        existing = make_product(name="Old Name")
        service, mock_repo, _ = make_service(found_product=existing)

        service.update_product("507f1e77bcf86cd799439011", {
            "name": "New Name",
            "price": 5999.0,
            "brand": "Keychron",
            "quantity": 30,
        })

        mock_repo.save.assert_called_once()

    def test_returns_none_when_product_not_found(self):
        service, _, _ = make_service(found_product=None)
        result = service.update_product("nonexistent", {"name": "X", "brand": "Y", "price": 1, "quantity": 1})
        assert result is None


# ─── delete_product ───────────────────────────────────────────

class TestDeleteProduct:

    def test_deletes_existing_product(self):
        service, mock_repo, _ = make_service()
        mock_repo.delete.return_value = True

        result = service.delete_product("507f1e77bcf86cd799439011")

        mock_repo.delete.assert_called_once_with("507f1e77bcf86cd799439011")
        assert result is True

    def test_returns_false_when_product_not_found(self):
        service, mock_repo, _ = make_service()
        mock_repo.delete.return_value = False

        result = service.delete_product("nonexistent")
        assert result is False