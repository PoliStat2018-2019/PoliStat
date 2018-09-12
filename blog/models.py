from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse 


class Post(models.Model):
    """
    Model representing a blog post.
    """

    title = models.CharField(max_length=128, unique=True)
    body = models.TextField()
    date_posted = models.DateField(default=timezone.now)

    class Meta:
        # most recent posts come first
        ordering = ['-date_posted']
    
    def get_absolute_url(self):
        """Return the URL through which this post is accessed."""
        return reverse('blog:view_post', args=[self.pk, self.slug()])

    # We use slugify to dynamically generate a slug for each post instead of
    # using models.SlugField() and storing the slug in the database.
    # The slug itself will not be used for a database lookup; instead, we 
    # will use the primary key, automatically generated as "post_id" in the
    # database.
    def slug(self):
        """Return a slugified version of the title."""
        return slugify(self.title)

    def __str__(self):
        """Return the title of this post as a string."""
        return self.title
