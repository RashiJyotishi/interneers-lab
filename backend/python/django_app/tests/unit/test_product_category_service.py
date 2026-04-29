import pytest
from unittest.mock import MagicMock
from django_app.core.services.product_category_service import ProductCategoryService
from django_app.core.models.product_category import ProductCategory


def make_category(**kwargs):
    defaults = dict(
        id="507f1e77bcf86cd799439011",
        title="Electronics",
        description="Electronic items",
    )
    defaults.update(kwargs)
    return ProductCategory(**defaults)


def make_service(found_category=None):
    mock_repo = MagicMock()
    mock_repo.find_by_id.return_value = found_category
    mock_repo.save.return_value = make_category()
    mock_repo.find_all.return_value = []
    mock_repo.delete.return_value = True
    return ProductCategoryService(repository=mock_repo), mock_repo


class TestCreateCategory:

    def test_creates_category_with_valid_data(self):
        service, mock_repo = make_service()
        service.create_category({"title": "Electronics", "description": "Gadgets"})
        mock_repo.save.assert_called_once()

    def test_raises_when_title_missing(self):
        service, _ = make_service()
        with pytest.raises(ValueError) as exc_info:
            service.create_category({"description": "No title here"})
        assert "title" in exc_info.value.args[0]

    def test_raises_when_title_empty_string(self):
        service, _ = make_service()
        with pytest.raises(ValueError) as exc_info:
            service.create_category({"title": "", "description": "Empty title"})
        assert "title" in exc_info.value.args[0]


class TestGetCategory:

    def test_returns_category_when_found(self):
        category = make_category(title="Food")
        service, mock_repo = make_service(found_category=category)

        result = service.get_category("507f1e77bcf86cd799439011")

        mock_repo.find_by_id.assert_called_once_with("507f1e77bcf86cd799439011")
        assert result.title == "Food"

    def test_returns_none_when_not_found(self):
        service, _ = make_service(found_category=None)
        result = service.get_category("nonexistent")
        assert result is None


class TestDeleteCategory:

    def test_deletes_existing_category(self):
        service, mock_repo = make_service()
        result = service.delete_category("507f1e77bcf86cd799439011")
        mock_repo.delete.assert_called_once_with("507f1e77bcf86cd799439011")
        assert result is True