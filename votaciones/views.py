from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from .models import Pregunta, Respuesta
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.db.models import F
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

# Create your views here.
# def index(request):
#     lista_preguntas_recientes = Pregunta.objects.order_by("-fecha_publicacion")[:4]
#     # template = loader.get_template("votaciones/index.html")
#     context = {
#         "lista_preguntas_recientes": lista_preguntas_recientes,
#     }
#     # return HttpResponse(template.render(context, request))
#     return render(request, "votaciones/index.html", context)


class IndexView(generic.ListView, LoginRequiredMixin):
    template_name = "votaciones/index.html"
    context_object_name = "lista_preguntas_recientes"

    def get_queryset(self):
        return Pregunta.objects.order_by("-fecha_publicacion")[:4]


# def detail(request, pregunta_id):
#     # try:
#     #     pregunta = Pregunta.objects.get(pk = pregunta_id)
#     # except Pregunta.DoesNotExist:
#     #     raise Http404("La pregunta no existe")
#     pregunta = get_object_or_404(Pregunta, pk = pregunta_id)
#     return render(request,"votaciones/detalle.html", {"pregunta": pregunta})
#     #return HttpResponse("Esta es la pregunta %s" % pregunta_id)

class DetailView(generic.DetailView, LoginRequiredMixin):
    model = Pregunta
    template_name = "votaciones/detalle.html"

# def results(request, pregunta_id):
#     pregunta = get_object_or_404(Pregunta, pk = pregunta_id)
#     return render(request, "votaciones/resultados.html",{"pregunta":pregunta})
#     #respuesta = "Estas viendo las respuestas de la pregunta %s"
#     #return HttpResponse(respuesta % pregunta_id)

class ResultView(generic.DetailView, LoginRequiredMixin):
    model = Pregunta
    template_name = "votaciones/resultados.html"

@login_required
def vote(request, pregunta_id):
    pregunta = get_object_or_404(Pregunta, pk = pregunta_id)
    try:
        respuesta_seleccionada = pregunta.respuesta_set.get(pk = request.POST["respuesta"])
    except(KeyError, Respuesta.DoesNotExist):
        return render(request, "votaciones/detalle.html", {"pregunta":pregunta, "error_message":"No has seleccionado una respuesta"})
    else:
        respuesta_seleccionada.votos = F("votos") + 1
        respuesta_seleccionada.save()
        return HttpResponseRedirect(reverse("votaciones:results", args=(pregunta_id,)))
    #return HttpResponse("Estas votando en la pregunta %s" % pregunta_id)