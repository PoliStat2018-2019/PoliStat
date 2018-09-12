from django.shortcuts import redirect, render, get_object_or_404

from .models import Post

def about(request):
    """Render the homepage of the Blog app."""
    
    return render(request, 'blog/about.html', {
        # about model? - Mark J. 9/12/18
    })

def view_post(request, post_id, slug):
    """Render an individual post."""

    # look up a Post by its id in the database
    post = get_object_or_404(Post, pk=post_id) 

    if slug != post.slug():
        return redirect('blog:view_post', post.pk, post.slug())
    
    return render(request, "blog/post.html", {
        "post": post
    })