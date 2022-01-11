from django.db import models


# Create your models here.
# 데이터베이스 저장 형식 (관리자)
class NewsData(models.Model):
    subject = models.CharField(max_length=200)
    category = models.CharField(max_length=25)
    create_date = models.DateTimeField()
    author = models.CharField(max_length=40, default='')
    content = models.TextField()
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return self.subject