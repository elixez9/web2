from django.contrib.auth.models import User


class EmailBackend:
    def authenticate(self, requests, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return
        except User.DoesNotExist:
            return None
