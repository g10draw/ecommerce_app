from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Profile
from .forms import (
    LoginForm, 
    UserRegistrationForm,
    UpdateUserForm, 
    UpdateProfileForm
)

@login_required
def profile(request):
    """ Updates user profile details """
    if request.method == 'POST':
        email = request.POST['email']
        user = None

        # Search for user
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            pass

        if user is None or user.id == request.user.id:
            user_form = UpdateUserForm(
                instance=request.user, 
                data=request.POST
            )
            profile_form = UpdateProfileForm(
                instance=request.user.profile,
                data=request.POST,
            )

            # Update profile details
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()

                messages.success(request, 'Profile was updated successfully')
        else:
            messages.error(request, 'User with given email already exists')

        return redirect('profile')

    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(
        request,
        'users/profile.html',
        {
            'user_form': user_form,
            'profile_form': profile_form
        }
    )


def register(request):
    """ Registers new user """
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            data = user_form.cleaned_data  # read form data

            email = data['email']
            password = data['password']
            password2 = data['password2']

            # compare both passwords
            if password == password2:
                # check for duplicate email
                if User.objects.filter(email=email).exists():
                    messages.error(request, 
                        'User with given email already exists')
                    return render(
                        request,
                        'users/register.html',
                        {'user_form': user_form}
                    )
            else:
                messages.error(request, 'Passwords don\'t match')
                return render(
                        request,
                        'users/register.html',
                        {'user_form': user_form}
                    )
            
            # Create a new user object
            new_user = User.objects.create_user(
                first_name=data['first_name'],
                last_name=data['last_name'],
                username=email,
                email=email,
                password=password
            )

            # Create the user profile
            Profile.objects.create(user=new_user)

            messages.success(request, 'Registration successful! Login now.')
            return redirect("/users/login/")
    else:
        user_form = UserRegistrationForm()
    return render(
        request,
        'users/register.html',
        {'user_form': user_form}
    )

def user_login(request):
    """ Logins users """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data  # read form data
            user_record = None
            # Search user by email
            try:
                user_record = User.objects.get(email=data['email'])
            except User.DoesNotExist:
                pass

            # Authenticate user
            if user_record:
                user = authenticate(
                    request,
                    username=user_record,
                    password=data['password']
                )

                if user is not None:
                    login(request, user)
                    return redirect('catalogue:product_list')
            # Inform user for wrong credentials
            messages.error(request, 'Incorrect email / password')
        
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})