import os

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404

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


@login_required
def delete_file(request, file_id):
    """
    Delete file by file ID.

    This method takes the request and file ID as parameters. It requires the user to be logged in.
    If the user is authenticated, the method retrieves the file object corresponding to the file ID and the user.
    If the request method is 'POST', the file is deleted and the user is redirected to the file list page.
    If the request method is not 'POST', the method renders the file confirm delete template,
     passing the file object as context.

    Parameters:
        - request (HttpRequest): The request object for this view.
        - file_id (int): The ID of the file to be deleted.

    Returns:
        - If the request method is 'POST', a redirect response to the file list page.
        - If the request method is not 'POST', a rendered response of the file confirm delete template.

    Raises:
        - Http404: If the file with the specified file ID and owner does not exist.

    Note:
        - The user must be logged in for this method to be accessible.
    """
    file = get_object_or_404(SharedFile, id=file_id, owner=request.user)
    if request.method == 'POST':
        file.delete()
        return redirect('file_list')
    return render(request, 'file_sharing/file_confirm_delete.html', {'file': file})
