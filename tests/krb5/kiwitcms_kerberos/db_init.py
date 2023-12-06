from django.contrib.auth.models import User

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
