from django.db import models
import django.contrib.auth.models as auth
from django.utils import timezone
from django.urls import reverse
from django.db.models.signals import post_save
from django.utils.html import strip_tags
from django.utils.functional import cached_property
from django.core.exceptions import ObjectDoesNotExist

from textwrap import dedent
import re

class User(auth.User):
    """User proxy to override the user manager."""

    manager = auth.UserManager()

    def __str__(self):
        return self.get_full_name()

    def __repr__(self):
        return "User[{}]".format(self.get_full_name())

    class Meta:
        proxy = True
        permissions = (
            ('manage_users', "Can manage user data and privileges"),
        )

class State(models.Model):
    """
    Model representing a U.S. state
    """

    manager = models.Manager()

    name = models.CharField(verbose_name='Name',
                            max_length=16,
                            primary_key=True,
                            unique=True)
    abbr = models.CharField(verbose_name='Abbreviation',
                            max_length=2,
                            unique=True)

    def __str__(self):
        return self.name
    
    @cached_property
    def num_districts(self):
        return District.manager.filter(state = self).count()
    
    def get_absolute_url(self):
        return reverse('figures:state', kwargs={
            'state': self.name
        })
    

class District(models.Model):
    """
    Model representing a U.S. state district
    """

    manager = models.Manager()

    # ForeignKey because a district belongs to only one State but
    # each State can have multiple districts
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    no = models.IntegerField(verbose_name='district number')

    id = models.IntegerField(default=1)

    name = models.CharField(verbose_name='district name',
                            max_length=8,
                            primary_key=True,
                            null=False)

    dem_nom = models.CharField(verbose_name='democratic nominee',
                               max_length=64,
                               blank=True)
    rep_nom = models.CharField(verbose_name='republican nominee',
                               max_length=64,
                               blank=True)
    modified = models.DateTimeField(verbose_name='last modified',
                                    auto_now=True,
                                    null=True)

    def __str__(self):
        """
        Return the name of the district as "State - District"
        """
        return f'{self.state.name} - {self.no}'

    @cached_property
    def short_name(self):
        """
        Returns 'SS-##' where SS is the state and ## is the district
        """
        if self.state.num_districts == 1:
            return f'{self.state.abbr}-AL'
        else:
            return f'{self.state.abbr}-{self.no:02d}'
    
    @cached_property
    def long_name(self):
        """
        'State's ##th district''
        """
        if self.state.num_districts == 1:
            return f'{self.state}\'s at-large district' 
        else:
            return f'{self.state}\'s {nth(self.no)} district'
    
    def get_absolute_url(self):
        return reverse('figures:district', kwargs={
            'districtno': self.no,
            'state': self.state.name
        })


class DistrictProfile(models.Model):
    """
    Model representing a district profile
    """

    manager = models.Manager()

    # Each district only has one profile (and each profile belongs
    # to only one district)
    district = models.OneToOneField(District,
                                    on_delete=models.CASCADE)

    profile = models.TextField()
    modified = models.DateTimeField(default=timezone.now)

    def get_profile_lead(self):
        stripped_profile = strip_tags(self.profile)
        stripped_profile = re.sub(r'(?<=[.,])(?=[^\s])', r' ',
                                  stripped_profile)

        return f'{stripped_profile}'[:128] + '...'

    def __str__(self):
        return f'{self.district} Profile'


class Prediction(models.Model):
    """
    Model representing a daily prediction
    """

    manager = models.Manager()

    district = models.ForeignKey(District, on_delete=models.CASCADE)
    dem_perc = models.FloatField(verbose_name=
                                 'democratic predicted percentage',
                                 default=0)
    rep_perc = models.FloatField(verbose_name=
                                 'republican predicted percentage',
                                 default=0)
    prediction_std = models.FloatField(verbose_name='prediction standard deviation', default=0)

    dem_win_percent = models.FloatField(verbose_name=
                                            'democratic win percent',
                                           default=0)
    rep_win_percent = models.FloatField(verbose_name=
                                            'republican win percentage',
                                           default=0)
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["date"]


class NationalPrediction(models.Model):
    """
    Model representing the national prediction
    """

    manager = models.Manager()

    dem_win_perc = models.FloatField(verbose_name='democratic win percent', default=.5)
    dem_average_seats = models.IntegerField(verbose_name='democratic predicted seats',default=217)

    histogram_data = models.TextField(verbose_name='histogram data',default='[]')

    date = models.DateTimeField(default=timezone.now)

# This method is required because we load districts from fixtures,
# which does not call the District.save() method. However, loaddata
# does send a post_save signal which we connect to here
def init_district_info(sender, instance, *args, **kwargs):
    """Every time a District is created, automatically create
    a DistrictProfile for it
    """

    profile_text = dedent("""
        This text is automatically generated for each district.
        Please change it soon.
    """)
    if District == sender:
        try:
            if not DistrictProfile.manager.get(district=instance):
                DistrictProfile.manager.get_or_create(
                    district=instance,
                    profile=profile_text
                )
        except ObjectDoesNotExist:
            DistrictProfile.manager.get_or_create(
                    district=instance,
                    profile=profile_text
                )
        Prediction.manager.get_or_create(
            district=instance
        )
post_save.connect(init_district_info)


class DistrictPost(models.Model):
    """
    Model representing a post

    A post is meant to be an update on any new district information
    such as new polls, unforseen factors, etc.
    """

    # ForeignKey because a post can only be about one district but each
    # district can have multiple posts
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    author = models.ForeignKey(User,
                                  on_delete=models.CASCADE)

    title = models.CharField(max_length=128, unique=True)
    body = models.TextField()


    date = models.DateField(default=timezone.now)

    class Meta:
        # order models by most recent first
        ordering = ['-date']
    
    # def get_absolute_url(self)

    def __str__(self):
        """Return the title of this post as a string"""
        return self.title


class BlogPost(models.Model):
    """
    Model representing a blog post

    A blog post is meant for student written assignments later on in
    the year such as specific candidates, current events, etc.
    """

    manager = models.Manager()

    title = models.CharField(max_length=200, unique=True)
    author = models.ForeignKey(User,
                              on_delete=models.CASCADE)
    body = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)

    class Meta:
        # order models by most recent first
        ordering = ['-date_posted']
    
    # def get_absolute_url(self)

    def __str__(self):
        """Return the title of this post as a string"""
        return self.title


def nth(n):
    """
    cardinal to ordinal
    """
    # from https://stackoverflow.com/questions/9647202/ordinal-numbers-replacement
    return "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])
