from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from app.models import UserProfile
import joblib
from django.core.files.storage import FileSystemStorage
from PIL import Image
import numpy as np
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


# Calculate BMI
def calculate_bmi(weight, height):
    return weight / (height**2)


# Determine health condition based on BMI
def determine_health_condition(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obesity"


# Process the uploaded image
def process_image(image):
    img = Image.open(image)
    img_array = np.array(img.resize((64, 64)))  # Resize or preprocess as needed
    return img_array


# HomePage view for processing images and generating PDFs
def HomePage(request):
    if request.method == "POST" and request.FILES.get("image"):
        image = request.FILES["image"]
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        uploaded_file_url = fs.url(filename)

        # Load models
        weight_model_path = "app\models\ weight_model.joblib"
        height_model_path = "app\models\height_model.joblib"
        weight_model = joblib.load(weight_model_path)
        height_model = joblib.load(height_model_path)

        # Process image and prepare data for prediction
        img_array = process_image(image)

        # Predict weight and height
        weight = weight_model.predict([img_array.flatten()])[0]
        height = height_model.predict([img_array.flatten()])[0]

        if weight <= 0 or height <= 0:
            return render(
                request, "home.html", {"error": "Invalid weight or height value"}
            )

        # Calculate BMI and health condition
        bmi = calculate_bmi(weight, height)
        health_condition = determine_health_condition(bmi)

        # Generate PDF report
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        p.drawString(100, 750, f"Uploaded Image: {filename}")
        p.drawString(100, 730, f"Weight: {weight:.2f} kg")
        p.drawString(100, 710, f"Height: {height:.2f} meters")
        p.drawString(100, 690, f"BMI: {bmi:.2f}")
        p.drawString(100, 670, f"Health Condition: {health_condition}")
        p.showPage()
        p.save()
        buffer.seek(0)

        response = HttpResponse(buffer, content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="bmi_report.pdf"'
        return response

    return render(request, "home.html")


# SignupPage view for user registration
def SignupPage(request):
    if request.method == "POST":
        uname = request.POST.get("username")
        email = request.POST.get("email")
        pass1 = request.POST.get("password1")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        domain = request.POST.get("domain")

        # Create the user
        my_user = User.objects.create_user(username=uname, email=email, password=pass1)
        my_user.save()
        print(f"User {my_user.username} with email {my_user.email} has been saved!")

        # Create the user profile
        profile = UserProfile(user=my_user, phone=phone, address=address, domain=domain)
        profile.save()
        print(
            f"User profile with phone {profile.phone}, address {profile.address}, domain {profile.domain}"
        )

        return redirect("login")

    return render(request, "signup.html")


# LoginPage view for user authentication
def LoginPage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        pass1 = request.POST.get("password")
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return HttpResponse("Username or Password is incorrect!")

    return render(request, "login.html")


# LogoutPage view for user logout
def LogoutPage(request):
    logout(request)
    return redirect("login")
