from django.shortcuts import render, redirect, get_object_or_404
from .models import Jasoseol, Comment
from .forms import JssForm, CommentForm
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
# from django.http import Http404

def index(request):
    all = Jasoseol.objects.all()
    return render(request, 'index.html', {'all_jss' : all})

def my_index(request):
    my = Jasoseol.objects.filter(author=request.user)
    return render(request, 'index.html', {'all_jss' : my})

@login_required(login_url='/login')
def create(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == "POST":
        filled_form = JssForm(request.POST)
        if filled_form.is_valid():
            temp_form = filled_form.save(commit=False)
            temp_form.author = request.user
            temp_form.save()
            return redirect('index')
    form = JssForm()
    return render(request, 'create.html', {'jss_form':form})

@login_required(login_url='/login')
def detail(request, jss_id):
    # try:
    #     my = Jasoseol.object.get(pk=jss_id)
    # except:
    #     raise Http404
    my = get_object_or_404(Jasoseol, pk=jss_id)
    comment = CommentForm()
    return render(request, 'detail.html', {'my_jss' : my, 'comment_form' : comment})

def delete(request, jss_id):
    my = Jasoseol.objects.get(pk=jss_id)
    if request.user == my.author:
        my.delete()
        return redirect('index')
    
    raise PermissionDenied

def update(request, jss_id):
    my = Jasoseol.objects.get(pk=jss_id)
    form = JssForm(request.POST, instance=my)
    if request.method == "POST":
        updated_form = JssForm(request.POST, instance=my)
        if updated_form.is_valid():
            updated_form.save()
            return redirect('index')
    return render(request, 'create.html', {'jss_form' : form})

def create_comment(request, jss_id):
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        temp_form = comment_form.save(commit=False)
        temp_form.author = request.user
        temp_form.jasoseol = Jasoseol.objects.get(pk=jss_id)
        temp_form.save()
        return redirect('detail', jss_id)

def delete_comment(request, jss_id, comment_id):
    my_comment = Comment.objects.get(pk=comment_id)
    if request.user == my_comment.author:
        my_comment.delete()
        return redirect('detail', jss_id)
    
    else:    
        raise PermissionDenied

def decode_base64(data):
    """Decode base64, padding being optional.

    :param data: Base64 data as an ASCII byte string
    :returns: The decoded byte string.

    """
    missing_padding = len(data) % 4 
    if missing_padding != 0:
        data += b'='* (4 - missing_padding)
    return base64.decodestring(data)