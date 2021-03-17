from django.db import models

# Create your models here.

class User(models.Model):   
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    birthday = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    email_verified_at = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    remember_token = models.CharField(max_length=255)
    created_at = models.CharField(max_length=255)
    updated_at = models.CharField(max_length=255)

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.name

class Post(models.Model):   
    post_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)        
    created_at = models.CharField(max_length=255)
    updated_at = models.CharField(max_length=255)

    class Meta:
        db_table = "posts"

    def __str__(self):
        return f'title:{self.title}'

class Comment(models.Model):   
    comment_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100)
    post_id = models.IntegerField()
    user_id = models.IntegerField()    
    created_at = models.CharField(max_length=255)
    updated_at = models.CharField(max_length=255)

    class Meta:
        db_table = "comments"

    def __str__(self):
        return f'title:{self.title}'

class Client(models.Model):   
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    birthday = models.DateTimeField()
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = "clients"

    def __str__(self):
        return self.name