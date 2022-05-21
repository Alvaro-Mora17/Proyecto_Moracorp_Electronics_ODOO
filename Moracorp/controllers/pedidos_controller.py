# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json

# Clase del controlador web



class ListaPedidos(http.Controller):
    
    '''
    Llamada web para obtener lista completa de los pedidos de nuestros clientes. No es parte de la API REST.
    
    
    Decorador que indica que la url "/gestion/pedidos/<modelo>" atendera por HTTP, sin autentificacion
    Devolvera texto que estará en formato JSON
    Se puede probar accediendo a http://localhost:8069/gestion/pedidos/moracorp.pedidos
    Y nos devolvera informacion sobre los pedidos
    '''

    @http.route('/gestion/pedidos/moracorp.pedidos', auth='public', cors='*', type='http')
    def obtenerDatosProveedores(self,**kw):
        # Obtenemos la referencia del modelo (pensado en este programa para ser "pedidos")
        pedidos = request.env['moracorp.pedidos'].sudo().search([])

        # Generamos la lista de pedidos
        lista_pedidos=[]
        for s in pedidos:
            estado = ""
            if s.estado == "categoria1":
              tipo = "En el Almacen"
            elif s.estado == "categoria2":
              tipo = "En Reparto"
            else:
              tipo = "Entregado"

            lista_pedidos.append({"id":s.id,"n_pedido":s.n_pedido,"venta":s.venta.n_transaccion,
            "distribuidor":s.distribuidor,"nif":s.nif,"nombre_cliente":s.nombre_cliente,
            "direccion_cliente":s.direccion_cliente,"telefono_cliente":s.telefono_cliente,
            "email_cliente":s.email_cliente,"mensajeria":s.mensajeria,"fecha_expedicion":s.fecha_expedicion,
            "fecha_recepcion":s.fecha_recepcion,"estado":tipo})
        json_result= http.Response(json.dumps(lista_pedidos, default=str),status=200,mimetype='application/json') 
        return json_result