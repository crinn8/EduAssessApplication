from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from django.core import exceptions as django_exceptions
from django.conf import settings

User = get_user_model()


class UserSerializer(BaseUserCreateSerializer):
    class Meta:
        model = User
        fields = '__all__'
        ref_name = 'UserSerializer'

    def validate(self, attrs):
        user = User(**attrs)
        password = attrs.get("password")

        if not self.instance and password:

            try:
                validate_password(password, user)
            except django_exceptions.ValidationError as e:
                serializer_error = serializers.as_serializer_error(e)
                raise serializers.ValidationError(
                    {"password": serializer_error["non_field_errors"]}
                )

        return attrs

    def create(self, validated_data):
        print(validated_data)
        # create the user instance
        user = super().create(validated_data)

        # send an email notification to the user
        subject = 'Account Created'
        html_message = render_to_string('account_created_email.html',
                                        {'user': user, 'password': validated_data.get('password')})
        plain_message = strip_tags(html_message)
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]
        send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)

        return user


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)
