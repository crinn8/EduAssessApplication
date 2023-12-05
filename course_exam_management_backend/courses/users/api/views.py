from rest_framework import generics, status
from rest_framework.generics import ListAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from users.api.serializers import UserSerializer, PasswordChangeSerializer
from users.filters import UserApiFilter
from users.models import User
from django.contrib.auth.hashers import check_password
from rest_framework.response import Response


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    model = User
    queryset = User.objects.all().distinct()
    filterset_class = UserApiFilter


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
