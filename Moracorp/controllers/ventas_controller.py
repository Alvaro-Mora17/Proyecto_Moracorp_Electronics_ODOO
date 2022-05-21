# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json

# Clase del controlador web



class ListaVentas(http.Controller):
    
    '''
    Llamada web para obtener lista completa de ventas de productos. No es parte de la API REST.
    
    
    Decorador que indica que la url "/gestion/ventas/<modelo>" atendera por HTTP, sin autentificacion
    Devolvera texto que estará en formato JSON
    Se puede probar accediendo a http://localhost:8069/gestion/ventas/moracorp.ventas
    Y nos devolvera informacion sobre cada venta de productos
    '''

    @http.route('/gestion/ventas/moracorp.ventas', auth='public', cors='*', type='http')
    def obtenerDatosVentas(self,**kw):
        # Obtenemos la referencia del modelo (pensado en este programa para ser "ventas")
        ventas = request.env['moracorp.ventas'].sudo().search([])

        # Generamos la lista de ventas
        lista_ventas=[]
        for s in ventas:
            informacion_productos = ""
            for i in range(len(s.productos)):
                if i == len(s.productos) - 1:
                    informacion_productos += " Nombre del Producto: " + s.productos[i].nombre + ", Cantidad Vendida: " + str(s.productos[i].cantidad_vendida) 
                elif i == 0:
                    informacion_productos += "Nombre del Producto: " + s.productos[i].nombre + ", Cantidad Vendida: " + str(s.productos[i].cantidad_vendida) +","
                else:
                    informacion_productos += " Nombre del Producto: " + s.productos[i].nombre + ", Cantidad Vendida: " + str(s.productos[i].cantidad_vendida) +","

            lista_ventas.append({'id':s.id,'n_transaccion':s.n_transaccion,'fecha_compra':s.fecha_compra,
            'cliente':s.cliente.nombre,'productos':informacion_productos,'precio_venta':"{0:.2f}".format(s.precio_venta)})
        json_result= http.Response(json.dumps(lista_ventas, default=str),status=200,mimetype='application/json') 
        return json_result