# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json

# Clase del controlador web



class ListaTransaccionVenta(http.Controller):
    
    '''
    Llamada web para obtener lista completa de las transacciones de venta de nuestros productos. No es parte de la API REST.
    
    
    Decorador que indica que la url "/gestion/ventas/transacciones/<modelo>" atendera por HTTP, sin autentificacion
    Devolvera texto que estará en formato JSON
    Se puede probar accediendo a http://localhost:8069/gestion/ventas/transacciones/moracorp.transaccion_venta
    Y nos devolvera informacion sobre las transacciones de venta
    '''

    @http.route('/gestion/ventas/transacciones/moracorp.transaccion_venta', auth='public', cors='*', type='http')
    def obtenerDatosProveedores(self,**kw):
        # Obtenemos la referencia del modelo (pensado en este programa para ser "transaccion_venta")
        transacciones = request.env['moracorp.transaccion_venta'].sudo().search([])

        # Generamos la lista de transacciones
        lista_transacciones=[]
        for s in transacciones:
            lista_transacciones.append({"id":s.id,"producto":s.producto.nombre,"cantidad_vendida":s.cantidad_vendida})
        json_result= http.Response(json.dumps(lista_transacciones, default=str),status=200,mimetype='application/json') 
        return json_result