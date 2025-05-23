import factory

from django.contrib.auth.models import User

from order.factories import Order

class UserFactory(factory.django.DjangoModelFactory):
    email = factory.faker('pystr')
    username = factory.faker('pystr')

    class Meta:
        model = User

class OrderFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)

    @factory.post_generation
    def product(self, create, extracted, **kwargs):
        if not create:
            return
        
        if extracted:
            for product in extracted:
                self.product.add(product)

    class Meta:
        model = Order
