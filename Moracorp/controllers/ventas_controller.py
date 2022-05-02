# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json

# Clase del controlador web



class ListaVentas(http.Controller):
    
    '''
    Llamada web para obtener lista completa de ventas de productos. No es parte de la API REST.
    
    
    Decorador que indica que la url "/gestion/<modelo>" atendera por HTTP, sin autentificacion
    Devolvera texto que estará en formato JSON
    Se puede probar accediendo a http://localhost:8069/gestion/moracorp.ventas
    Y nos devolvera informacion sobre cada venta de productos
    '''

    @http.route('/gestion/ventas/<modelo>', auth='public', cors='*', type='http')
    def obtenerDatosVentas(self, modelo, **kw):
        # Obtenemos la referencia del modelo (pensado en este programa para ser "ventas")
        ventas = request.env[modelo].sudo().search([])

        #Generamos la lista de cargamentos
        lista_ventas=[]
        for s in ventas:
            lista_ventas.append(s.read())
        json_result= http.Response(json.dumps(lista_ventas, default=str)[1:-1].replace("], [",","),status=200,mimetype='application/json') 
        return json_result