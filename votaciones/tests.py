import datetime

from django.utils import timezone
from django.test import TestCase
from votaciones.models import Pregunta, Respuesta
from django.urls import reverse

def crear_pregunta(texto_pregunta, dias):
    return Pregunta.objects.create(texto_pregunta = texto_pregunta, fecha_publicacion=timezone.now() + datetime.timedelta(days = dias))

class RespuestaModelTest(TestCase):
    def test_crear_respuesta_para_pregunta(self):
        pregunta = Pregunta(texto_pregunta="¿Te gusta viajar?", fecha_publicacion=timezone.now())
        pregunta.save()
        respuesta = Respuesta(pregunta=pregunta, texto_respuesta="Sí", votos=0)
        respuesta.save()
        self.assertEqual(respuesta.pregunta, pregunta)

    def test_eliminar_pregunta_con_sus_respuestas(self):
        pregunta = Pregunta(texto_pregunta="¿Cómo estás?", fecha_publicacion=timezone.now())
        pregunta.save()
        respuesta = Respuesta(pregunta=pregunta, texto_respuesta="Bien", votos=0)
        respuesta.save()

        pregunta_id = pregunta.id
        respuesta_id = respuesta.id
        pregunta.delete()

        with self.assertRaises(Pregunta.DoesNotExist):
            Pregunta.objects.get(pk=pregunta_id)

        with self.assertRaises(Respuesta.DoesNotExist):
            Respuesta.objects.get(pk=respuesta_id)

class PreguntaIndexViewTest(TestCase):
    def test_no_hay_preguntas(self):
        respuesta = self.client.get(reverse("votaciones:index"))
        print(respuesta)
        self.assertEqual(respuesta.status_code, 200)
        self.assertQuerySetEqual(respuesta.context["lista_preguntas_recientes"], [])

    def test_preguntas(self):
        pregunta = crear_pregunta("Te gusta la comida mexicana", dias=10)
        respuesta = self.client.get(reverse("votaciones:index"))
        self.assertQuerySetEqual(respuesta.context["lista_preguntas_recientes"], [pregunta])

class PreguntaDetailView(TestCase):
    def test_pregunta(self):
        pregunta = crear_pregunta("Como estas?", dias=-10)
        url = reverse("votaciones:detail", args=(pregunta.id, ))
        respuesta = self.client.get(url)
        self.assertContains(respuesta, pregunta.texto_pregunta)