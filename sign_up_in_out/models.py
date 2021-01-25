from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.CharField(max_length=100)

    def __str__(self):
        return "[name=%s, email=%s]" % (self.name, self.email)

class Blog(models.Model):
    subject = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateField(auto_now_add = True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)

    def __str__(self):
        return self.subject