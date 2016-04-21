#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models

class URL(models.Model): #Quitamos la 's' de URLs, porque ya la añade django.
	direccion_URL = models.CharField(max_length = 100)