import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailChangeForm(forms.Form):
    new_email = forms.EmailField(
        label="新しいメールアドレス",
        widget=forms.EmailInput(attrs={"placeholder": "例:new@example.com"})
    )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_new_email(self):
        email = self.cleaned_data["new_email"].strip()
        if self.user and self.user.email and email.lower() == self.user.email.lower():
            raise forms.ValidationError("現在のメールアドレスと同じです。")

        qs = User.objects.filter(email__iexact=email)
        if self.user:
            qs = qs.exclude(pk=self.user.pk)
        if qs.exists():
            raise forms.ValidationError("このメールアドレスはすでに使用されています。")
        return email


class SignupForm(UserCreationForm):
    email = forms.EmailField(label="メールアドレス")

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        labels = {
            "username": "ユーザーネーム",
            "password1": "パスワード",
            "password2": "パスワード（確認要）",
        }

    def clean_password1(self):
        password = self.cleaned_data.get("password1")

        if not (8 <= len(password) <= 64):
            raise forms.ValidationError(
                "パスワードは8文字以上64文字以内で入力してください。"
            )
        if not re.match(r'^[\21-\x7E]+$', password):
            raise forms.ValidationError(
                "パスワードは半角英数字記号のみ使用できます。"
            )
        return password