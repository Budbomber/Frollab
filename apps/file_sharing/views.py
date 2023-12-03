from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from apps.file_sharing.forms import FileUploadForm
from apps.file_sharing.models import SharedFile


# Create your views here.
def file_list(request):
    files = SharedFile.objects.all()  # Adjust the query as needed
    return render(request, 'file_sharing/file_list.html', {'files': files})
@login_required
def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            shared_file = form.save(commit=False)
            shared_file.uploaded_by = request.user
            shared_file.save()
            return redirect('file_list')
    else:
        form = FileUploadForm()
    return render(request, 'file_sharing/file_upload.html', {
        'form': form
    })


