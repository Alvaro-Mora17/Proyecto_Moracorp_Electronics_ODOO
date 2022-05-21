# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json

# Clase del controlador web



class ListaCompras(http.Controller):
    
    '''
    Llamada web para obtener lista completa de compras de productos. No es parte de la API REST.
    
    
    Decorador que indica que la url "/gestion/compras/<modelo>" atendera por HTTP, sin autentificacion
    Devolvera texto que estará en formato JSON
    Se puede probar accediendo a http://localhost:8069/gestion/compras/moracorp.compras
    Y nos devolvera informacion sobre cada compra de productos
    '''

    @http.route('/gestion/compras/moracorp.compras', auth='public', cors='*', type='http')
    def obtenerDatosCompras(self,**kw):
        # Obtenemos la referencia del modelo (pensado en este programa para ser "compras")
        compras = request.env['moracorp.compras'].sudo().search([])

        # Generamos la lista de compras
        lista_compras=[]
        for s in compras:
            lista_compras.append({'id':s.id,'n_transaccion':s.n_transaccion,'proveedor':s.proveedor.nombre,
            'fecha_compra':s.fecha_compra,'fecha_entrega':s.fecha_entrega,'producto':s.producto.nombre,
            'precio_unidad':"{0:.2f}".format(s.precio_unidad),'porcentaje_iva':s.porcentaje_iva,'precio_iva':"{0:.2f}".format(s.precio_iva),
            'cantidad':s.cantidad,'precio_total':"{0:.2f}".format(s.precio_total)})
        json_result= http.Response(json.dumps(lista_compras, default=str),status=200,mimetype='application/json') 
        return json_result
    
    # Actualizamos el Stock al realizar una Compra desde la Aplicacion Moracorp hecha con el Framework Quasar
    # Se puede probar accediendo a http://localhost:8069/gestion/compras/actualizar/moracorp.compras
    
    @http.route('/gestion/compras/actualizar/moracorp.compras', auth='public', cors='*',type='http')
    def actualizarStockCompras(self,**kw):
        compras = request.env['moracorp.compras'].sudo().search([])
        for recordcompra in compras:
            recordcompra.actualizoRegistrosCompras()
        return 'Actualizacion del Stock Completada'
        
