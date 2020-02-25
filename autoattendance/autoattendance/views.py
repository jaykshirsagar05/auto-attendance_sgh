from django.shortcuts import render
import pyrebase

config = {
    'apiKey': "AIzaSyCTBN5WXkpfmIp0uDqHhVgyHXzZ5tcDglM",
    'authDomain': "autoattendance-91502.firebaseapp.com",
    'databaseURL': "https://autoattendance-91502.firebaseio.com",
    'projectId': "autoattendance-91502",
    'storageBucket': "autoattendance-91502.appspot.com",
    'messagingSenderId': "421526185934",
    'appId': "1:421526185934:web:97b3b65cbb88a3e5efed9f",
    'measurementId': "G-SNJVZR5PXN"
}

firebase = pyrebase.initialize_app(config)

auth = firebase.auth()

def signIn(request):

    return render(request, "hello.html")

def postsignIn(request):

    email = request.POST.get('email')
    passw = request.POST.get('password')

    user = auth.sign_in_with_email_and_password(email, passw)

    return render(request, "welcome.html", {"em": email})

# just for practice

# Jay's practice for updation