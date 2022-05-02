# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json

# Clase del controlador web



class ListaStock(http.Controller):
    
    '''
    Llamada web para obtener lista completa del stock de los productos. No es parte de la API REST.
    
    
    Decorador que indica que la url "/gestion/<modelo>" atendera por HTTP, sin autentificacion
    Devolvera texto que estará en formato JSON
    Se puede probar accediendo a http://localhost:8069/gestion/moracorp.productos
    Y nos devolvera informacion sobre el stock de cada producto
    '''

    @http.route('/gestion/stock/<modelo>', auth='public', cors='*', type='http')
    def obtenerDatosStock(self, modelo, **kw):
        # Obtenemos la referencia del modelo (pensado en este programa para ser "productos")
        stocks = request.env[modelo].sudo().search([])

        #Generamos la lista de cargamentos
        lista_stock=[]
        for s in stocks:
            lista_stock.append(s.read())
        json_result= http.Response(json.dumps(lista_stock, default=str)[1:-1].replace("], [",","),status=200,mimetype='application/json') 
        return json_result