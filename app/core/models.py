from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin
from django.conf import settings


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Committee(models.Model):
    committee = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.committee


class Bill(models.Model):
    bill = models.CharField(max_length=80, blank=True, unique=True)
    committee = models.ForeignKey(Committee, related_name='bills', on_delete=models.CASCADE, blank=True)
    lastupdated = models.CharField(max_length=10, blank=True, null=True)
    count = models.IntegerField(null=True)

    class Meta:
        db_table = 'bill'

    def __str__(self):
        return self.bill


class Billview(models.Model):
    NORMAL = 'NORM'
    ALTERNATIVE = 'ALT'
    DISCARDED = 'DISC'

    STATUS_TYPE = (
        (NORMAL, '의안'),
        (ALTERNATIVE, '대안'),
        (DISCARDED, '대안반영폐기'),
    )

    billno = models.IntegerField(primary_key=True)
    billname = models.CharField(max_length=80, blank=True, null=True)
    billlink = models.CharField(max_length=34, blank=True, null=True)
    proposerkind = models.CharField(max_length=10, blank=True, null=True)
    proposerdt = models.CharField(max_length=10, blank=True, null=True)
    submitdt = models.CharField(max_length=10, blank=True, null=True)
    procdt = models.CharField(max_length=10, blank=True, null=True)
    generalresult = models.CharField(max_length=10, blank=True, null=True)
    summarycontent = models.TextField(blank=True, null=True)
    billstep = models.CharField(max_length=10, blank=True, null=True)
    finished = models.BooleanField(blank=True, null=True)
    done = models.BooleanField(blank=True, null=True)
    coactors = models.TextField(blank=True, null=True)
    bill = models.ForeignKey(Bill, related_name='billviews', on_delete=models.CASCADE, blank=True)
    committee = models.ForeignKey(Committee, related_name='billviews', on_delete=models.CASCADE, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_TYPE, default=NORMAL)
    alternative = models.ForeignKey('self', null=True, related_name='billviews', on_delete=models.SET_NULL)
    lastupdated = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        db_table = 'billview'

    def __str__(self):
        return str(self.billno)


class Subscribe(models.Model):
    """User can subscribe a law"""
    subscribe_bill = models.ForeignKey(Bill, related_name='subscribes', on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.subscribe_bill)


class Bookmark(models.Model):
    """User can bookmark a bill"""
    bookmark = models.ForeignKey(Billview, related_name='bookmarks', on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.bookmark)
