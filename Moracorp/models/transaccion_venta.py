# -*- coding: utf-8 -*-

from odoo import models, fields, api

#Definimos el modelo de datos
class Transaccion_Venta(models.Model):
    #Nombre y descripcion del modelo de datos
    _name = 'moracorp.transaccion_venta'
    _description = 'Modelo de Transaccion de Venta'
    #Herencia Delegada del Modelo de Productos
    _inherits = {'moracorp.productos': 'producto'}

    #Elementos de cada fila del modelo de datos
    id = fields.Integer()
    producto = fields.Many2one('moracorp.productos')
    cantidad_vendida = fields.Integer(string ="Cantidad de Productos Vendidos")

    #Sobreescribo el metodo editar
    def write(self,values):
        result = super(Transaccion_Venta,self).write(values)
        #Añado esto: llamo a la funcion que actualiza el registro de venta
        for recordventa in self.env['moracorp.ventas'].search([]):
            recordventa.actualizoRegistrosVentas()
            recordventa.total_venta()
        #hago lo normal del metodo editar
        return result

    
