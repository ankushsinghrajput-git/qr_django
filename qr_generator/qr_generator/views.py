from django.shortcuts import render
from .forms import QRCodeForm
import qrcode
import os
from django.conf import settings


def generate_qr_code(request):
    if request.method == "POST":
        form = QRCodeForm(request.POST)
        if form.is_valid():
            qr_name = form.cleaned_data["name"]
            qr_url = form.cleaned_data["url"]

            # Generate QR Code
            qr = qrcode.make(qr_url)
            filename = qr_name.replace(" ", "_").lower() + "_qr.png"
            filepath = os.path.join(settings.MEDIA_ROOT, filename)
            qr.save(filepath)

            # QR URL
            generated_qr_url = os.path.join(settings.MEDIA_URL, filename)

            context = {
                "qr_name": qr_name.upper(),
                "generated_qr_url": generated_qr_url,
                "filename": filename,
            }
            return render(request, "qr_result.html", context)

    else:
        form = QRCodeForm()
        context = {
            "form": form,
        }
        return render(request, "generate_qr_code.html", context)
