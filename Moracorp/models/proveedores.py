# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date

# Definimos el modelo de datos
class Proveedores(models.Model):
    # Nombre y descripcion del modelo de datos
    _name = 'moracorp.proveedores'
    _description = 'Modelo de Proveedores'

    '''Indicamos que cuando se necesite un nombre, se usara el atributo nombre'''
    _rec_name="nombre"

    # Elementos de cada fila del modelo de datos
    id = fields.Integer()
    cif = fields.Char('Codigo de Identificacion Fiscal(CIF)')
    nombre = fields.Char(string ="Nombre del Proveedor")
    foto = fields.Image(max_width=175,max_height=175)
    fecha_fundacion = fields.Date(string = "Fecha de Fundacion")
    tipo_sociedad = fields.Selection(
        [('categoria1', 'Sociedad de Responsabilidad Limitada (S.L.)'),
         ('categoria2', 'Sociedad Anónima (S.A.)'),
         ('categoria3', 'Sociedad Colectiva (S.C.)'),
         ('categoria4', 'Sociedad Cooperativa')],
        required=True)
    direccion = fields.Char(string = "Direccion del Proveedor")
    codigo_postal = fields.Char(string = "Codigo Postal")
    telefono = fields.Char()
    email = fields.Char()
    sede = fields.Char(string = "Sede Central")

    # Aplicamos una restriccion sobre el campo cif para que sea unico
    _sql_constraints = [
        ('cif_uniq', 'UNIQUE (cif)', 'El Codigo de Identificacion Fiscal del Proveedor debe ser único.')
    ]

    # Aplicamos una restriccion al campo fecha_fundacion para que la fecha de fundacion no sea posterior o igual a la fecha actual
    @api.constrains('fecha_fundacion')
    def check_fecha_fundacion(self):
        for record in self:
            if record.fecha_fundacion  and record.fecha_fundacion >= date.today():
                raise models.ValidationError('Error la Fecha de Fundacion no  puede ser mayor o igual a la Fecha Actual.')

                
    