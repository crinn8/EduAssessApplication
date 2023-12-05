from django.contrib.auth import password_validation
from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet

from users.api.serializers import UserSerializer, PasswordChangeSerializer
from users.filters import UserApiFilter
from users.models import User
from django.contrib.auth.hashers import check_password, make_password
from rest_framework.response import Response
from django.core.exceptions import ValidationError as CoreValidationError


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    model = User
    queryset = User.objects.all().distinct()
    filterset_class = UserApiFilter

    @action(methods=['post'], detail=False, url_path="password_reset", authentication_classes=[],
            permission_classes=[AllowAny])
    def password_reset(self, request, pk=None):
        print(request.data)
        if not request.data.get('email'):
            raise ValidationError({'email': ['This field is required']})
        if not request.data.get('password'):
            raise ValidationError({'password': ['This field is required']})
        user = get_object_or_404(User, email=request.data.get('email'))
        if user:
            try:
                password_validation.validate_password(request.data.get('password'))
                password = make_password(request.data.get('password'))
                user.password = password
                user.save()
            except CoreValidationError as error:
                raise ValidationError({'password': [error]})
            serializer = self.get_serializer(user, many=False)
            return Response(serializer.data)
        else:
            raise ValidationError({'email': ['User Not Exist']})


class PasswordChangeView(generics.UpdateAPIView):
    serializer_class = PasswordChangeSerializer
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get the user based on the currently logged-in user
        user = self.request.user

        # Check if the old password provided matches the user's current password
        if not check_password(serializer.validated_data['old_password'], user.password):
            return Response({'old_password': ['Incorrect password.']},
                            status=status.HTTP_400_BAD_REQUEST)

        # Check if the new password and confirmation match
        if serializer.validated_data['new_password'] != serializer.validated_data['confirm_password']:
            return Response({'confirm_password': ["New passwords don't match."]},
                            status=status.HTTP_400_BAD_REQUEST)

        # Update the user's password
        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response({'detail': 'Password changed successfully.'},
                        status=status.HTTP_200_OK)
