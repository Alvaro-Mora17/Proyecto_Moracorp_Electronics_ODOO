# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json

# Clase del controlador web



class ListaStock(http.Controller):
    
    '''
    Llamada web para obtener lista completa del stock de los productos. No es parte de la API REST.
    
    
    Decorador que indica que la url "/gestion/stock/<modelo>" atendera por HTTP, sin autentificacion
    Devolvera texto que estará en formato JSON
    Se puede probar accediendo a http://localhost:8069/gestion/stock/moracorp.productos
    Y nos devolvera informacion sobre el stock de cada producto
    '''

    @http.route('/gestion/stock/moracorp.productos', auth='public', cors='*', type='http')
    def obtenerDatosStock(self,**kw):
        # Obtenemos la referencia del modelo (pensado en este programa para ser "productos")
        stocks = request.env['moracorp.productos'].sudo().search([])

        # Generamos la lista de stock de productos
        lista_stock=[]
        for s in stocks:
            lista_stock.append({"id":s.id,"nombre":s.nombre,"cantidad":s.cantidad,"compra":s.compra
            ,"venta":s.venta,"ingresos":"{0:.2f}".format(s.ingresos),"costes":"{0:.2f}".format(s.costes)
            ,"beneficios":"{0:.2f}".format(s.beneficios)})
        json_result= http.Response(json.dumps(lista_stock, default=str),status=200,mimetype='application/json') 
        return json_result