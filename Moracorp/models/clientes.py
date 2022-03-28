# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date

#Definimos el modelo de datos
class Clientes(models.Model):
    #Nombre y descripcion del modelo de datos
    _name = 'moracorp.clientes'
    _description = 'Modelo de Clientes'
    #Como no tenemos un atributo "name" en nuestro modelo, indicamos que cuando
    #se necesite un nombre, se usara el atributo tarea
    _rec_name="id"

    #Elementos de cada fila del modelo de datos
    id = fields.Integer(string ="Nº de Socio")
    nif = fields.Char(string ="Numero de Identificacion Fiscal(NIF)")
    nombre = fields.Char()
    foto = fields.Image(max_width=100,max_height=100)
    fecha_registro = fields.Date(string = "Fecha de Registro")
    direccion = fields.Char()
    telefono = fields.Char()
    codigo_postal = fields.Char()
    localizacion = fields.Char()

    _sql_constraints = [
        ('nif_uniq', 'UNIQUE (nif)', 'El Numero de Identificacion Fiscal del Cliente debe ser único.')
    ]

    # Aplicamos una restriccion al campo fecha_registro para que la fecha de registro no sea posterior a la fecha actual
    @api.constrains('fecha_registro')
    def check_fecha_registro(self):
        for record in self:
            if record.fecha_registro  and record.fecha_registro > date.today():
                raise models.ValidationError('Error la Fecha de Registro no puede ser mayor a la Fecha Actual.')
