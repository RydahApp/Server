# import factory
# from django.contrib.auth import get_user_model

# User = get_user_model()

# class AdminFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = User
    
#     email = factory.Sequence(lambda n: f'admin{n}@example.com')

#     @factory.post_generation
#     def set_password(obj, create, extracted, **kwargs):
#         password = 'admin123'
#         obj.set_password(password)
#         obj.save()
        
#     @factory.post_generation
#     def make_superuser(obj, create, extracted, **kwargs):
#         if not create:
#             return
        
#         obj.is_superuser = True
#         obj.is_admin = True
#         obj.save()