from django.shortcuts import render, redirect
from .models import User, Blog
import re, hmac

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return USER_RE.match(username)

PASSWORD_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return PASSWORD_RE.match(password)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
    return EMAIL_RE.match(email)



secret_key = 'secret'

def hashed_uid(uid):
    return "%s|%s" % (uid, hmac.new(secret_key.encode('utf-8'), uid.encode('utf-8')).hexdigest())

def check_hashed_uid(h):
    uid = h.split('|')[0]
    if h == hashed_uid(uid):
        return uid



def signup(request):
    username = ""
    email = ""
    username_msg = ""
    password_msg = ""
    verify_msg = ""
    email_msg = ""

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        verify = request.POST.get('verify')
        email = request.POST.get('email')
        error = False

        if not username or not valid_username(username):
            username_msg = "Please provide a valid username."
            error = True
        elif User.objects.filter(name__exact=username):
            username_msg = "Username already exist."
            error = True
        if not password or not valid_password(password):
            password_msg = "Please provide a valid password."
            error = True
        if not verify == password:
            verify_msg = "Passwords do not match."
            error = True
        if email:
            if not valid_email(email):
                email_msg = "Please provide a valid email."
                error = True
            elif User.objects.filter(email__exact=email):
                email_msg = "Email already exist."
                error = True

        if not error:
            u = User(name = username, password = password, email = email)
            u.save()
            response = redirect("../blog")
            response.set_cookie('user_id', hashed_uid(str(u.pk)))
            return response

    context = {
        "title": "Signup",
        "username": username,
        "username_msg": username_msg,
        "password_msg": password_msg,
        "verify_msg": verify_msg,
        "email": email,
        "email_msg": email_msg
    }
    return render(request, "signup.html", context)

def signin(request):
    username = ""
    error_msg = ""

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        error = False

        if User.objects.filter(name__exact=username):
            if not password == User.objects.get(name__exact=username).password:
                error = True
        else:
            error = True

        if error:
            error_msg = "Invalid login"
        else:
            response = redirect("../blog")
            response.set_cookie('user_id', hashed_uid(str(User.objects.get(name__exact=username).pk)))
            return response

    context = {
        "title": "Signin",
        "username": username,
        "error_msg": error_msg
    }
    return render(request, 'signin.html', context)

def blog(request):
    # Check whether the user_id cookie is set
    hashed_user_id = request.COOKIES.get('user_id')
    if not hashed_user_id:
        return redirect("../signup")
    user_id = check_hashed_uid(hashed_user_id)
    if not user_id:
        return redirect("../signup")

    username = User.objects.get(pk__exact=user_id).name

    context = {
        "title": "Welcome %s" % username,
        "user_name": username,
        "blogs": Blog.objects.all()
    }
    return render(request, "blog.html", context)

def newpost(request):
    # Check whether the user_id cookie is set
    hashed_user_id = request.COOKIES.get('user_id')
    if not hashed_user_id:
        return redirect("../../signup")
    user_id = check_hashed_uid(hashed_user_id)
    if not user_id:
        return redirect("../../signup")

    subject = ""
    content = ""
    error_msg = ""

    if request.method == 'POST':
        subject = request.POST.get('subject')
        content = request.POST.get('content')
        if subject and content:
            user = User.objects.get(pk__exact=check_hashed_uid(request.COOKIES.get('user_id')))
            b = Blog(subject = subject, content = content, user = user)
            b.save()
            return redirect("../")
        else:
            error_msg = "Subject and content, please!"
        if not subject:
            subject = ""
        if not content:
            content = ""

    context = {
        "title": "New Post",
        "subject": subject,
        "content": content,
        "error_msg": error_msg
    }
    return render(request, "newpost.html", context)

def myposts(request):
    # Check whether the user_id cookie is set
    hashed_user_id = request.COOKIES.get('user_id')
    if not hashed_user_id:
        return redirect("../../signup")
    user_id = check_hashed_uid(hashed_user_id)
    if not user_id:
        return redirect("../../signup")

    user = User.objects.get(pk__exact=user_id)

    context = {
        "title": "My Post",
        "blogs": Blog.objects.filter(user__exact=user)
    }
    return render(request, "mypost.html", context)

def welcome(request):
    hashed_user_id = request.COOKIES['user_id']
    user_id = check_hashed_uid(hashed_user_id)
    if not user_id:
        return redirect("../../signup")

    username = User.objects.get(pk__exact=user_id).name

    context = {
        "title": "Welcome",
        "username": username
    }
    return render(request, "welcome.html", context)

def signout(request):
    response = redirect('../../signup')
    response.set_cookie('user_id', '')
    return response
