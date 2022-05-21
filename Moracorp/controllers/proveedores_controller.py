# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json

# Clase del controlador web



class ListaProveedores(http.Controller):
    
    '''
    Llamada web para obtener lista completa de los proveedores de productos. No es parte de la API REST.
    
    
    Decorador que indica que la url "/gestion/proveedores/<modelo>" atendera por HTTP, sin autentificacion
    Devolvera texto que estará en formato JSON
    Se puede probar accediendo a http://localhost:8069/gestion/proveedores/moracorp.proveedores
    Y nos devolvera informacion sobre el proveedor de cada producto
    '''

    @http.route('/gestion/proveedores/moracorp.proveedores', auth='public', cors='*', type='http')
    def obtenerDatosProveedores(self,**kw):
        # Obtenemos la referencia del modelo (pensado en este programa para ser "proveedores")
        proveedores = request.env['moracorp.proveedores'].sudo().search([])

        # Generamos la lista de proveedores
        lista_proveedores=[]
        for s in proveedores:
            tipo = ""
            if s.tipo_sociedad == "categoria1":
              tipo = "Sociedad de Responsabilidad Limitada (S.L.)"
            elif s.tipo_sociedad == "categoria2":
              tipo = "Sociedad Anónima (S.A.)"
            elif s.tipo_sociedad == "categoria3":
              tipo = "Sociedad Colectiva (S.C.)"
            else:
              tipo = "Sociedad Cooperativa"
    
            lista_proveedores.append({"id":s.id,"cif":s.cif,"nombre":s.nombre,"fecha_fundacion":s.fecha_fundacion,
            "tipo_sociedad": tipo ,"direccion":s.direccion,"codigo_postal":s.codigo_postal,"telefono":s.telefono,
            "email":s.email,"sede":s.sede})
        json_result= http.Response(json.dumps(lista_proveedores, default=str),status=200,mimetype='application/json') 
        return json_result