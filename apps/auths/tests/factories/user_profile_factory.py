# import factory
# import factory.fuzzy
# from apps.auths.models import UserProfile
# # from .user_factory import User

# class UserProfileFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = UserProfile
    
#     user = factory.SubFactory('apps.auths.tests.factories.UserFactory')
#     first_name = 'Test1'
#     last_name = 'Last1'
#     username = factory.Sequence(lambda n: f'username{n}')
#     mobile_no = factory.Faker('phone_number')
#     email = factory.LazyAttribute(lambda o: o.user.email)
#     location = factory.Faker('address')
