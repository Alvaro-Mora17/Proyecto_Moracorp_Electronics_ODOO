# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json

# Clase del controlador web



class ListaClientes(http.Controller):
    
    '''
    Llamada web para obtener lista completa de los clientes que compraron nuestros productos. No es parte de la API REST.
    
    
    Decorador que indica que la url "/gestion/clientes/<modelo>" atendera por HTTP, sin autentificacion
    Devolvera texto que estará en formato JSON
    Se puede probar accediendo a http://localhost:8069/gestion/clientes/moracorp.clientes
    Y nos devolvera informacion sobre los clientes
    '''

    @http.route('/gestion/clientes/moracorp.clientes', auth='public', cors='*', type='http')
    def obtenerDatosProveedores(self,**kw):
        # Obtenemos la referencia del modelo (pensado en este programa para ser "clientes")
        clientes = request.env['moracorp.clientes'].sudo().search([])

        # Generamos la lista de clientes
        lista_clientes=[]
        for s in clientes:
            lista_clientes.append({"id":s.id,"nif":s.nif,"nombre":s.nombre,"fecha_registro":s.fecha_registro,
            "direccion":s.direccion,"telefono":s.telefono,"email":s.email,"codigo_postal":s.codigo_postal,
            "localizacion":s.localizacion})
        json_result= http.Response(json.dumps(lista_clientes, default=str),status=200,mimetype='application/json') 
        return json_result