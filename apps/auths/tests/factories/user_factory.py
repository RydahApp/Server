import factory
from django.contrib.auth import get_user_model
from apps.auths.models import UserProfile
from django.db.models.signals import post_save
from faker import Faker
fake = Faker()

User = get_user_model()

@factory.django.mute_signals(post_save)
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        
    first_name = 'Test1'
    last_name = 'Last1'
    email = factory.Sequence(lambda n: f'test{n}@example.com')
    username = factory.Sequence(lambda n: f'username{n}')
    password = factory.PostGenerationMethodCall('set_password', 'defaultpassword')
    is_verified=True
    is_active=True
    profile = factory.RelatedFactory('apps.auths.tests.factories.user_factory.UserProfileFactory', factory_related_name='user')
    
    @factory.post_generation
    def create_profile(self, created, extracted, **kwargs):
        if not created:
            # Only create the profile if the user is created
            return
        if extracted:
            # Override default profile attributes if needed
            self.profile = UserProfileFactory(user=self, **kwargs)

class UserProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserProfile
    
    first_name = factory.LazyAttribute(lambda o: o.user.first_name)
    last_name = factory.LazyAttribute(lambda o: o.user.last_name)
    email = factory.LazyAttribute(lambda o: o.user.email)
    username = factory.LazyAttribute(lambda o: o.user.username)
    user = factory.SubFactory(UserFactory, profile=None)
    mobile_no = factory.Faker('numerify', text='###########')
    location = factory.Faker('address')

    
class AdminFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    
    email = factory.Sequence(lambda n: f'admin{n}@example.com')

    @factory.post_generation
    def set_password(obj, create, extracted, **kwargs):
        password = 'admin123'
        obj.set_password(password)
        obj.save()
        
    @factory.post_generation
    def make_superuser(obj, create, extracted, **kwargs):
        if not create:
            return
        
        obj.is_superuser = True
        obj.is_admin = True
        obj.save()