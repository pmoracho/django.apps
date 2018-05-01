from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


# from django.shortcuts import render
# from django.shortcuts import redirect
# from django.conf import settings
# from django.core.files.storage import FileSystemStorage
# from .forms import DocumentForm
# from .forms import ComprobanteForm

# # Create your views here.
# def home(request):
#     return render(request, 'main/index.html')


# def simple_upload(request):
#     if request.method == 'POST' and request.FILES['myfile']:
#         myfile = request.FILES['myfile']
#         fs = FileSystemStorage()
#         filename = fs.save(myfile.name, myfile)
#         uploaded_file_url = fs.url(filename)
#         return render(request, 'main/simple_upload.html', {
#             'uploaded_file_url': uploaded_file_url
#         })
#     return render(request, 'main/simple_upload.html')

# def model_form_upload(request):
#     if request.method == 'POST':
#         form = ComprobanteForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = ComprobanteForm()
#     return render(request, 'main/model_form_upload.html', {
#         'form': form
#     })
