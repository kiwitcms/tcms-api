from django.contrib.auth.models import User
from django.contrib.auth.models import Permission

from tcms.management.models import Classification
from tcms.utils.permissions import initiate_user_with_default_setups


# this will be used for API calls
bot = User.objects.create(
    username="kiwitcms-bot",
    email="info@example.com",
    is_active=True,
)
bot.set_password("changeme")
bot.save()
initiate_user_with_default_setups(bot)

# this is used inside integration test
Classification.objects.create(name="test-products")

# account only to verify credentials passed
# via Python source code, not config file
developer = User.objects.create(
    username="kiwitcms-developer",
    email="developler@example.com",
    is_active=True,
)
developer.set_password("hack-me")
developer.save()
initiate_user_with_default_setups(developer)
developer.user_permissions.add(
    Permission.objects.get(content_type__app_label="auth", codename="view_user")
)
