from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from member.models import Member, MemberCategory, MemberVerification

class MemberCategoryInline(admin.TabularInline):
    model = MemberCategory

class MemberCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."))

    class Meta:
        model = Member
        fields = ("username",)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(MemberCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class MemberAdmin(UserAdmin):
    add_form = MemberCreationForm
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name','phone','photo')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
    )

    inlines = [MemberCategoryInline]

    list_display = ('id', 'email', 'username', 'first_name', 'last_name', 'is_active', 'is_staff','is_superuser','photo','phone','updated_at','date_joined')

admin.site.register(Member, MemberAdmin)

@admin.register(MemberVerification)
class MemberVerificationAdmin(admin.ModelAdmin):
    list_display = ('id','member','code','verified','created_at','updated_at')