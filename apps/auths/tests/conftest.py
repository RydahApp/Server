from pytest_factoryboy import register
# from .factories import user_factory
from .factories.user_factory import UserFactory
from .factories.user_factory import AdminFactory
from .factories.user_factory import UserProfileFactory


register(UserFactory)
register(AdminFactory)
register(UserProfileFactory)