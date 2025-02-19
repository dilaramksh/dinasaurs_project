from django.shortcuts import render, redirect
from social_media.forms.ImageUploadForm import ImageUploadForm
from social_media.models import profile_pictures

def profile_pictures(request):
    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES)  # ✅ Correct instantiation
        if form.is_valid():
            uploaded_image = form.save()
            return render(request, "upload_success.html", {"image_url": uploaded_image.image.url})
    else:
        form = ImageUploadForm()  # ✅ Correct instantiation

    return render(request, "upload.html", {"form": form})