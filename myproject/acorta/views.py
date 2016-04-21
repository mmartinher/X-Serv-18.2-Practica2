#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts             import render
from django.http                  import HttpResponse, HttpResponseNotFound
from django.http                  import HttpResponseRedirect, HttpResponseBadRequest
from models                       import URL
from django.views.decorators.csrf import csrf_exempt
from django.template.loader       import get_template
from django.template              import Context

@csrf_exempt
def acortar(request):
	if request.method == "GET":  
		URLs_guardadas = URL.objects.all()
		plantilla_principal = get_template("pagina_principal.html")
		Context = ({'lista_urls': URLs_guardadas})
		return HttpResponse(plantilla_principal.render(Context))

	elif request.method == "POST":
		url = request.POST.get("url")
		if url == "":
			mensaje = "Está vacío"
			plantilla_error = get_template("pagina_error.html")
			Context = ({'mensaje': mensaje})
			return HttpResponseBadRequest(plantilla_error.render(Context))

		elif not url.startswith("http://") and not url.startswith("https://"):
			url = "http://" + url

		try:
			nueva_URL = URL.objects.get(direccion_URL=url)

		except URL.DoesNotExist:
			nueva_URL = URL(direccion_URL=url)
			nueva_URL.save()
		plantilla_seleccion = get_template("pagina_seleccion.html")
		id = nueva_URL.id
		Context = ({'id': id})
		return HttpResponse(plantilla_seleccion.render(Context))

	else:
		mensaje = "Algo ha ido mal"
		plantilla_error = get_template("pagina_error.html")
		Context = ({'mensaje': mensaje})
		return HttpResponse(plantilla_error.render(Context))

def redireccionar(request, id):
	try:
		direccion = URL.objects.get(id=id)
	except URL.DoesNotExist:
		mensaje = "La página no existe"
		plantilla_error = get_template("pagina_error.html")
		Context = ({'mensaje': mensaje})
		return HttpResponseNotFound(plantilla_error.render(Context))
	return HttpResponseRedirect(direccion.direccion_URL)