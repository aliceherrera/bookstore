import pytest

from product.models import Product

@pytest.mark.django_db
def test_create_product():
    product = Product.objects.create(
        title = "Teste produto 01",
        description = "Descrição produto 01",
        price = 150
    )

    assert product.title == "Teste produto 01"
    assert product.description == "Descrição produto 01"
    assert product.price == 150
    assert product.id is not None