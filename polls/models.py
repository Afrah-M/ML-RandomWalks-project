from django.db import models
from django.utils import timezone

# Create your models here.



class Attribute(models.Model):
    attribute_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    # def __str__(self):
     #  return self.question_text
       #  def was_published_recently(self):
   # now = timezone.now()
    #return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Value(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    value_text = models.CharField(max_length=200)
    values = models.FloatField(default=0.0)
    # def __str__(self):
       #  return self.choice_text
