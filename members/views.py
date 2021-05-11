from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from .forms import SignUpForm, EditProfileForm, PasswordChangingForm, ProfileEditPageForm

from myBlog.models import UserProfile


# Create your views here.

class UserRegisterView(generic.CreateView):
    form_class = SignUpForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')


class UserEditView(generic.UpdateView):
    form_class = EditProfileForm
    template_name = 'registration/edit_profile.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user


class PasswordsChangeView(PasswordChangeView):
    # form_class = PasswordChangeForm
    form_class = PasswordChangingForm
    template_name = 'registration/change_password.html'
    success_url = reverse_lazy('password_success')


def password_success(request):
    return render(request, 'registration/password_success.html', {})


class ShowProfilePageView(generic.DetailView):
    model = UserProfile
    template_name = 'registration/user_profile.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ShowProfilePageView, self).get_context_data(*args, **kwargs)
        page_user = get_object_or_404(UserProfile, id=self.kwargs.get('pk'))
        context['page_user'] = page_user
        return context


class EditProfilePageView(generic.UpdateView):
    model = UserProfile
    # form_class = ProfileEditPageForm
    template_name = 'registration/edit_profile_page.html'
    fields = ['bio', 'profile_picture', 'website_url', 'facebook_url', 'twitter_url', 'insta_url', 'pinterest_url', ]
    success_url = reverse_lazy('home')


class CreateProfilePAgeView(generic.CreateView):
    model = UserProfile
    form_class = ProfileEditPageForm
    template_name = "registration/create_profile_page.html"

    ### if you are gonna use form comment fields ###
    # fields = '__all__'

    # overwriting the form that being processed and pass the current user id
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
