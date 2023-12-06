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
    """
    List all shared files.

    This method retrieves all shared files from the database and renders them to the 'file_list.html' template.

    Parameters:
        request (HttpRequest): The request object from the user.

    Returns:
        HttpResponse: The rendered response with the files displayed in the 'file_list.html' template.
    """
    files = SharedFile.objects.all()  # Adjust the query as needed
    return render(request, 'file_sharing/file_list.html', {'files': files})


@login_required
def upload_file(request):
    """
    Uploads a file to the file sharing application.

    Parameters:
    - request: The HTTP request object.
    - Returns: The HTTP response object.

    Example usage:

        upload_file(request)

    This method is used to handle the file upload functionality in the file sharing application. It requires the user
     to be logged in.

    On receiving a POST request, the method validates the file upload form submitted by the user. If the form is valid,
    a new SharedFile object is created and saved to the database with the owner set to the currently logged in user.
    The method then redirects the user to the 'file_list' view.

    On receiving a GET request, the method initializes an empty FileUploadForm and renders the 'file_upload.html'
    template with the form as context.

    Note: This method requires the login_required decorator from django.contrib.auth.decorators to enforce
    user authentication.

    """
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
    """
    Downloads a file from the server.

    Parameters:
        request (HttpRequest): The HTTP request object.
        file_id (int): The ID of the file to be downloaded.

    Returns:
        HttpResponse: The HTTP response object containing the file content.

    Raises:
        Http404: If the file does not exist.

    Example usage:

        # Assuming file_id = 1
        response = download_file(request, 1)
    """
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
