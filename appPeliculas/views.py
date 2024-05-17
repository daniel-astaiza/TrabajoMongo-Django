from django.shortcuts import render
from django.conf import settings;
from django.db import Error;
from appPeliculas.models import Genero, Pelicula
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.shortcuts import render, redirect
import os
from bson import ObjectId
# Create your views here.

def inicio(request):
    return render(request, "inicio.html")

def vistaAgregarGenero(request):
    return render(request, "agregarGenero.html")


@csrf_exempt
def agregarGenero(request):
    try:
        nombre = request.POST["nombre"]
        #crear objeto de tipo genero
        genero = Genero(genNombre = nombre)
        #salvar el objeto, lo que permite
        #crear en la base de datos 
        genero.save()
        mensaje="genero agregado correctamente"
        
    except Error as error:
        mensaje = str(error)
    retorno={"mensaje" : mensaje}
    
    
    # return JsonResponse(retorno)
    return render (request , "agregarGenero.html", retorno)

def listarPeliculas(request):
    peliculas = Pelicula.objects.all()
    retorno ={"peliculas" : peliculas}
    
    return render (request , "listarPeliculas.html" , retorno)


# @csrf_exempt
@csrf_exempt
def agregarPelicula(request):
    try:
        codigo = request.POST["Codigo"]
        titulo = request.POST["Titulo"]
        protaginista = request.POST["Protagonista"]
        duracion = int(request.POST["Duracion"])
        resumen = request.POST["Resumen"]
        foto = request.FILES["Foto"]
        idGenero = ObjectId(request.POST["Genero"])
        genero = Genero.objects.get(pk=ObjectId(idGenero))
        #crear objeto de la pelicula 
        pelicula = Pelicula(pelCodigo=codigo,
                            pelTitulo= titulo,
                            pelProtagonista=protaginista,
                            pelDuracion= duracion,
                            pelResumen=resumen,
                            pelFoto=foto,
                            pelGenero = genero
                            )
        pelicula.save()
        mensaje ="pelicula agregada correctamente"
            
    except Error as error:
        mensaje = str(error)
    
    retorno={"mensaje" : mensaje, "idPelicula": pelicula.pk}
    
    return redirect ("/listarPeliculas")

def vistaAgregarPelicula(request):
    generos =Genero.objects.all()
    retorno={"generos": generos}
    return render(request , "agregarPelicula.html" , retorno)


def consultarPeliculaPorId(request , id):
    pelicula = Pelicula.objects.get(pk=ObjectId(id))
    generos = Genero.objects.all()
    #se retorna los generos por que se necesita la interfaz
    retorno ={"pelicula": pelicula, "generos": generos}
    return render(request, "actualizarPelicula.html", retorno)


def actualizarPelicula(request):
    try:
        idPelicula = ObjectId(request.POST['idPelicula'])
        #se obtiene la pelicula a partir del id
        peliculaActualizar = Pelicula.objects.get(pk=idPelicula)
        #actualizar los demas campos
        peliculaActualizar.pelCodigo=request.POST["Codigo"]
        peliculaActualizar.pelTitulo= request.POST["Titulo"]
        peliculaActualizar.pelProtagonista=request.POST["Protagonista"]
        peliculaActualizar.pelDuracion=int(request.POST["Duracion"])
        peliculaActualizar.pelResumen=request.POST["Resumen"]
        
        idGenero = ObjectId(request.POST["Genero"])
        genero = Genero.objects.get(pk=idGenero)
        peliculaActualizar.pelGenero = genero 
        foto = request.FILES.get ("foto")
        
        if (foto):
            if( peliculaActualizar.pelFoto):
                os.remove(os.path.join(settings.MEDIA_ROOT + "/" + 
                                   str(peliculaActualizar.pelFoto)))
            peliculaActualizar.pelFoto = foto 
            
        peliculaActualizar.save()
        mensaje = "pelicula actualizada"
    except Error as error:
        mensaje = str(error)
    retorno ={"mensaje": mensaje}
    # return JsonResponse(retorno)        
    return redirect("/listarPeliculas")


def eliminarPelicula (request , id):
    try:
        peliculAEliminar = Pelicula.objects.get(pk=ObjectId(id))
        peliculAEliminar.delete()
        mensaje = "Pelicula Eliminada"
        
    except Error as error:
        mensaje = str(error)
    retorno = {"mensaje": mensaje}
    # return JsonResponse (retorno)
    return redirect("/listarPeliculas")
        