from django.db import models

class Problem(models.Model):
	
	problem_text = models.TextField()
	title = models.CharField(max_length=200)
	url = models.CharField(max_length=200)
	mem_limit = models.CharField(max_length=15)
	description = models.TextField()
	problem_input = models.TextField()
	problem_output = models.TextField()
	time_limit = models.CharField(max_length=15)