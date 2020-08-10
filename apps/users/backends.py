from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth import get_user_model

from apps.users.models import CustomUser

UserModel = get_user_model()


class AuthModelBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        if username is None or password is None:
            return
        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'phone': username}
        try:
            #user = CustomUser.objects.get(**kwargs)
            user = UserModel.objects.get(Q(email=username) | Q(phone=username))
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
