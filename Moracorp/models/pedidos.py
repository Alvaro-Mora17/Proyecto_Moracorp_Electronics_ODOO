# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date

#Definimos el modelo de datos
class Pedidos(models.Model):
    #Nombre y descripcion del modelo de datos
    _name = 'moracorp.pedidos'
    _description = 'Modelo de Pedidos'
    #Como no tenemos un atributo "name" en nuestro modelo, indicamos que cuando
    #se necesite un nombre, se usara el atributo tarea
    _rec_name="n_pedido"

    #Elementos de cada fila del modelo de datos
    id = fields.Integer()
    n_pedido = fields.Char(string = "Nº de Pedido")
    venta = fields.Many2one('moracorp.ventas',string = "Identificador de la Venta")
    distribuidor = fields.Char(string = "Distribuidor",default='Moracorp Electronics',readonly = 'True')
    nif = fields.Char(string = 'NIF del Cliente',compute="datos_cliente", store=True)
    nombre_cliente = fields.Char(string = 'Nombre del Cliente',compute="datos_cliente", store=True)
    mensajeria = fields.Char(string = "Empresa de Logistica")
    fecha_expedicion = fields.Date(string = "Fecha de Expedicion",compute="datos_cliente", store=True)
    fecha_recepcion = fields.Date(string = "Fecha de Recepcion")
    estado = fields.Selection(
        [('categoria1', 'En el Almacen'),
         ('categoria2', 'En Reparto'),
         ('categoria3', 'Entregado')],
        required=True)

    _sql_constraints = [
        ('n_pedido_uniq', 'UNIQUE (n_pedido)', 'El Numero de Pedido debe ser único.')
    ]

    @api.depends('venta')
    def datos_cliente(self):
        for pedidos in self:
            for recordventa in self.env['moracorp.ventas'].search([]):
                if pedidos.venta.n_transaccion == recordventa.n_transaccion:
                    pedidos.nif = recordventa.cliente.nif
                    pedidos.nombre_cliente = recordventa.cliente.nombre
                    pedidos.fecha_expedicion = recordventa.fecha_compra
            
            
    # Aplicamos una restriccion al campo fecha_registro para que la fecha de registro no sea posterior a la fecha actual
    @api.constrains('fecha_recepcion')
    def check_fecha_recepcion(self):
        for record in self:
            if record.fecha_recepcion and record.fecha_recepcion < record.fecha_expedicion:
                raise models.ValidationError('Error la Fecha de Recepcion no puede ser menor a la Fecha de Expedicion.')
