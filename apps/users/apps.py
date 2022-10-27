from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.users'         # `users` -> `apps.users`，否则报错`RuntimeError: Model class apps.users.models.Users doesn't declare an explicit app_label and isn't in an application in INSTALLED_APPS.`
