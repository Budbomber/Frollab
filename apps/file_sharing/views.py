import os

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from apps.file_sharing.forms import FileUploadForm
from apps.file_sharing.models import SharedFile


# Create your views here.
@login_required
def file_list(request):
    files = SharedFile.objects.all()  # Adjust the query as needed
    return render(request, 'file_sharing/file_list.html', {'files': files})


@login_required
def upload_file(request):
    
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            shared_file = form.save(commit=False)
            shared_file.owner = request.user
            shared_file.save()
            return redirect('file_list')
    else:
        form = FileUploadForm()
    return render(request, 'file_sharing/file_upload.html', {
        'form': form
    })


@login_required
def download_file(request, file_id):
    
    file = SharedFile.objects.get(id=file_id)
    file_path = file.file.path
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/octet-stream")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


@require_POST
@login_required
def delete_file(request, file_id):
    file = get_object_or_404(SharedFile, id=file_id, owner=request.user)
    file.delete()
    return redirect('file_list')
