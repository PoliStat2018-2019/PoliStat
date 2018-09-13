from django.db import models
from django.utils import timezone


class State(models.Model):
    """
    Model representing a U.S. state
    """

    name = models.CharField(max_length=16, unique=True)
    abbr = models.CharField(max_length=2, unique=True)


class District(models.Model):
    """
    Model representing a U.S. state district
    """

    # ForeignKey because a district belongs to only one State but
    # each State can have multiple districts
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    no = models.IntegerField(verbose_name='district number')
    dem_nom = models.CharField(verbose_name='democratic nominee',
                               max_length=64)
    rep_nom = models.CharField(verbose_name='republican nominee',
                               max_length=64)

    # prediction
    # last updated
    # graphs? - Mark J. 9/12/18

    def __str__(self):
        """
        Return the name of the district as "State - District 12"
        
        E.g. "Mississippi - District 3"
        """
        return f'{self.state.name} - District {self.no}'


class DistrictProfile(models.Model):
    """
    Model representing a district profile
    """

    # Each district only has one profile (and each profile belongs
    # to only one district)
    district = models.OneToOneField(District,
                                    on_delete=models.CASCADE)

    profile = models.TextField()
    modified = models.DateField(default=timezone.now)


class Post(models.Model):
    """
    Model representing a post

    A post is meant to be an update on any new district information
    such as new polls, unforseen factors, etc.
    """

    # ForeignKey because a post can only be about one district but each
    # district can have multiple posts
    district = models.ForeignKey(District, on_delete=models.CASCADE)

    title = models.CharField(max_length=128, unique=True)
    body = models.TextField()
    date_posted = models.DateField(default=timezone.now)

    class Meta:
        # order models by most recent first
        ordering = ['-date_posted']
    
    # def get_absolute_url(self)

    def __str__(self):
        """Return the title of this post as a string"""
        return self.title
        