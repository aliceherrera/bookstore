import factory

from product.models import Product, Category


class CategoryFactory(factory.django.DjangoModelFactory):
    title = factory.Faker('word')
    slug = factory.Faker('slug')
    description = factory.Faker('sentence')
    active = factory.Iterator([True, False])

    class Meta:
        model = Category

class ProductFactory(factory.django.DjangoModelFactory):
    price = factory.Faker('pydecimal', left_digits=4, right_digits=2, positive=True)
    category = factory.SubFactory(CategoryFactory)
    title = factory.Faker('sentence')

    @factory.post_generation
    def category(self, create, extracted, **kwargs):
        if not create:
            return
        
        if extracted:
            for category in extracted:
                self.category.add(category)

    class Meta:
        model = Product
