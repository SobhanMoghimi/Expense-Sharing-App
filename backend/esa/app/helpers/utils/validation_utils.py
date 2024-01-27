import re

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from esa.app.helpers.exceptions.exceptions import InvalidPhoneNumberException


class ValidationUtils:
    @staticmethod
    def validate_phone_number(phone_number: str):
        if not re.match('\+[9][8][9]\d{9}$', phone_number):
            raise InvalidPhoneNumberException

    @staticmethod
    def validate_password(password):
        if len(password) < 8:
            raise serializers.ValidationError("Make sure your password is at least 6 letters")
        elif re.search('[a-z]', password) is None:
            raise serializers.ValidationError("Make sure your password has a lower letter in it")
        elif re.search('[A-Z]', password) is None:
            raise serializers.ValidationError("Make sure your password has a capital letter in it")
        elif re.search(
                "[\\!\\\"\\#\\$\\%\\&\\'\\(\\)\\*\\+\\,\\-\\.\\/\\:\\;\\<\\>\\=\\?\\@\\[\\]\\{\\}\\\\\\^\\_\\`\\~]",
                password) is None:
            raise serializers.ValidationError("Make sure your password has a symbol letter in it")

    @staticmethod
    def validate_otp_code(code):
        match_obj = re.match('\\d{6}$', code)
        if not match_obj:
            raise serializers.ValidationError("code is invalid")

    @staticmethod
    def validate_persian(value: str) -> bool:
        match_obj: re.Match = re.match("^[\u0600-\u06FF\uFB8A\u067E\u0686\u06AF]+$", value)
        if not match_obj:
            raise ValidationError("Make sure your input is persian")

    @staticmethod
    def validate_email(email):
        match_obj: re.Match = re.match(
            "(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])",
            email)
        if not match_obj:
            raise ValidationError("invalid email")

    @staticmethod
    def validate_positive_amount(amount):
        if amount <= 0:
            raise ValidationError("Must be a positive value")

    @staticmethod
    def validate_first_and_last_name(name):
        if not all(char.isalpha() or char.isspace() for char in name):
            raise ValidationError("make sure to use characters for first name and last name")
