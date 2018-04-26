# Cristina del Río
from django.shortcuts import render
from cms_barrapunto.models import Pages
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys
import urllib.request

FORMULARIO= """
<form action="" method="POST">
    <u><b>Name: </b></ul><br><input type="text" name="name"><br>
    <u><b>Page: </b></ul><br><input type="text" name="page"/><br>
    <input type="submit" value="Enviar"/>
</form>"""

contenido_Rss = ""

class myContentHandler(ContentHandler):

    def __init__ (self):
        self.inItem = False
        self.inContent = False
        self.theContent = ""

    def startElement (self, name, attrs):
        if name == 'item':
            self.inItem = True
        elif self.inItem:
            if name == 'title':
                self.inContent = True
            elif name == 'link':
                self.inContent = True
            
    def endElement (self, name):
        global contenido_Rss
        if name == 'item':
            self.inItem = False
        elif self.inItem:
            if name == 'title':
                self.title = "Title: " + self.theContent + "."
                print(self.title)  # imprimes el titulo
                # To avoid Unicode trouble
                self.inContent = False
                self.theContent = ""
            elif name == 'link':
                self.link = " Link: " + self.theContent + "."
                contenido_Rss += "<ul><li>"
                contenido_Rss += "<a href=" + self.theContent + ">"
                contenido_Rss += self.title + "</a><br>\n"
                contenido_Rss += "</ul></li>"
                self.inContent = False
                self.theContent = ""

    def characters (self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars

def inicio_pag(request):
    resp = "<u><h4>La lista de las paginas es:</h4></u>"
    list_pags = Pages.objects.all()
    for pag in list_pags:
        resp +=  "<ul><li>" + pag.name + " ==> " + pag.page + "</ul></li>"
    return HttpResponse(resp)
 
  
@csrf_exempt
def pag(request, ident):
    if request.method == "GET":
        try:
			# Cuando existe
            page = Pages.objects.get(name=ident)
            resp = "La página que has pedido es: " + page.name + " ==> " + page.page
            resp +=	"<br>Su contenido es" + contenido_Rss
        except Pages.DoesNotExist:
			# Cuando no existe
            resp = "Esta página no existe, puedes crearla:" + FORMULARIO    
    elif request.method == "POST":
        name = request.POST['name']
        page = request.POST['page']
        pagina = Pages(name=name, page=page)
        pagina.save()
        resp = "Has creado la página: <b>" + name + "</b><br> Su id es : <b>" + str(pagina.id) + "</b>"
        
    else:
        resp = "Método no permitido"
    return HttpResponse(resp)


def update(request):
    theParser = make_parser()
    theHandler = myContentHandler()
    theParser.setContentHandler(theHandler)
    url = "http://barrapunto.com/index.rss"
    fich = urllib.request.urlopen(url)
    theParser.parse(fich)
    resp = "<html><body><div>Las noticias que hay son: " + contenido_Rss
    resp += "</div></body></html>"
    return HttpResponse(resp)
