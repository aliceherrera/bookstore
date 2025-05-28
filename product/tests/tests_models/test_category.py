import pytest

from product.models import Category

@pytest.mark.django_db
def test_create_category():
    category = Category.objects.create(
        title = "Teste categoria 01",
        slug = "Teste categoria slug 01",
        description = "Descrição categoria 01",
    )

    assert category.title == "Teste categoria 01"
    assert category.slug == "Teste categoria slug 01"
    assert category.description == "Descrição categoria 01"
    assert category.active is True
