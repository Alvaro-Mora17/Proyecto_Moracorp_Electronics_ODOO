# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json
import re

# Clase del controlador web



class BorrarDatos(http.Controller):

    '''
    Llamada web que nos permite borrar todos los registros que deseemos de los modelos de la Empresa Moracorp Electronics. No es parte de la API REST.
    
    
    Decorador que indica que la url "/gestion/borrar/<modelo>/<id>" atendera por HTTP, sin autentificacion
    Devolvera texto que estará en formato JSON
    Se puede probar accediendo a http://localhost:8069/gestion/borrar/moracorp.productos/1
    '''
    
    @http.route('/gestion/borrar/<model>/<id>', auth='public', cors='*',csrf=False,type='http')
    def EliminarProductos(self,model,id,**kw):
        datos = request.env[model].sudo().search([])
        for dato in datos:
            if dato.id == int(id):
                dato.unlink()
                return '<h1>Elemento Borrado</h1>'
        return '<h1>Error ID no Encontrado</h1>'
