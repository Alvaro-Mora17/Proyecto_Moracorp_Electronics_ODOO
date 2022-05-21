# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json
import re

# Clase del controlador web



class ListaProductos(http.Controller):
    
    '''
    Llamada web para obtener lista completa de productos. No es parte de la API REST.
    
    
    Decorador que indica que la url "/gestion/<modelo>" atendera por HTTP, sin autentificacion
    Devolvera texto que estará en formato JSON
    Se puede probar accediendo a http://localhost:8069/gestion/moracorp.productos
    Y nos devolvera informacion sobre cada producto
    '''

    @http.route('/gestion/moracorp.productos', auth='public', cors='*',type='http')
    def obtenerDatosProductos(self,**kw):
        # Obtenemos la referencia del modelo (pensado en este programa para ser "productos")
        productos = request.env["moracorp.productos"].sudo().search([])

        # Generamos la lista de productos
        lista_productos=[]
        for s in productos:
            patron = re.compile(s.descripcion)
            if not patron.search('<.*?>'):
                descripcion = re.sub(re.compile('<.*?>') ,"",s.descripcion)
            else:
                descripcion = s.descripcion
                
            lista_productos.append({'id':s.id,'n_serie':s.n_serie,'nombre':s.nombre,'marca':s.marca.nombre,
            'descripcion':descripcion,'precio':"{0:.2f}".format(s.precio),'porcentaje_iva':s.porcentaje_iva,
            'precio_iva':"{0:.2f}".format(s.precio_iva)})
        json_result= http.Response(json.dumps(lista_productos, default=str),status=200,mimetype='application/json') 
        return json_result