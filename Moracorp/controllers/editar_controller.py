# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json

# Clase del controlador web


class EditarDatos(http.Controller):
    
    '''
    Llamada web que nos permite editar todos los registros que deseemos de los modelos de la Empresa Moracorp Electronics. No es parte de la API REST.
    
    
    Decorador que indica que la url "/gestion/editar/<modelo>" atendera por HTTP, sin autentificacion
    Devolvera texto que estará en formato JSON
    Se puede probar accediendo a http://localhost:8069/gestion/editar/moracorp.productos?data={"id":"1","nombre":"Prueba"}
    '''

    @http.route('/gestion/editar/<model>', auth='public', cors='*',csrf=False, type='http')
    def editarDatos(self,**args):
        # Obtenemos el modelo de los argumentos
        model = args['model']

        # Pasamos lo recibido en "data" a un diccionario
        dicDatos=json.loads(args['data'])
        # Si se ha indicado id, hay busqueda
        if dicDatos["id"]:
            search = [('id', '=', int(dicDatos["id"]))]
        else:
            return "{'estado':'DATO NO INDICADO'}"
        record = http.request.env[model].sudo().search(search)
        if record and record[0]:
                record[0].write(dicDatos)
                # Devolvemos el registro creado, siguiendo este esquema
                return http.Response(
                    json.dumps(
                    
                        record.read(), # Lectura del registro
                        default=str # Funcion de conversion por defecto (str, para convertir a String elementos como los datetime)
                        ),
                        status=200, # Respuesta de la aplicación al navegador
                        mimetype='application/json'
                    )
            # Caso de que el registro no sea encontrado
        return "Registro no encontrado"
