# -*- coding: utf-8 -*-

from odoo import models, fields, api

#Definimos el modelo de datos
class Productos(models.Model):
    #Nombre y descripcion del modelo de datos
    _name = 'moracorp.productos'
    _description = 'Modelo de Productos'
    
    #Como no tenemos un atributo "name" en nuestro modelo, indicamos que cuando
    #se necesite un nombre, se usara el atributo tarea
    _rec_name="nombre"

    #Elementos de cada fila del modelo de datos
    id = fields.Integer()
    n_serie = fields.Char(string ="Nº de Serie")
    nombre = fields.Char()
    foto = fields.Image(max_width=175,max_height=175)
    descripcion = fields.Html('Descripcion',sanitaze=True,strp_style=False)
    marca = fields.Many2one('moracorp.proveedores')
    cantidad = fields.Integer(string = "Cantidad en Stock ",compute="stock", store=True)
    posible_compra = fields.Integer()
    posible_venta = fields.Integer()
    compra = fields.Integer(compute="productos_compra", store=True)
    venta = fields.Integer(compute="productos_venta", store=True)
    precio = fields.Float(string = "Precio sin IVA")
    porcentaje_iva = fields.Float(string = "Porcentaje de IVA")
    precio_iva = fields.Float(string = "Precio de Venta al Publico(PVP)",compute="agregar_iva", store=True)
    posible_coste = fields.Float()
    posible_ingreso = fields.Float()
    ingresos = fields.Float(compute="producto_ingresos", store=True)
    costes = fields.Float(compute="producto_costes", store=True)
    beneficios = fields.Float(compute="producto_beneficios", store=True)
    video = fields.Char(string = "URL del Video")

    # Aplicamos una restriccion sobre el campo numero de serie para que sea unico
    _sql_constraints = [
        ('n_serio_uniq', 'UNIQUE (n_serie)', 'El Número de Serie debe ser único.')
    ]

    # Saca el precio del producto con iva dependiendo del precio sin iva y el porcentaje de iva
    @api.depends('precio','porcentaje_iva')
    def agregar_iva(self):
        for record in self:
            record.precio_iva = record.precio + (record.precio * (record.porcentaje_iva / 100))

    @api.depends('posible_compra')
    def productos_compra(self):
        for record in self:
            record.compra = record.posible_compra

    @api.depends('posible_venta')
    def productos_venta(self):
        for record in self:
            record.venta = record.posible_venta
    
    @api.depends('compra','venta')
    def stock(self):
        for record in self:
            record.cantidad = record.compra - record.venta
    
    @api.depends('posible_coste')
    def producto_costes(self):
        for record in self:
            record.costes = record.posible_coste

    @api.depends('posible_ingreso')
    def producto_ingresos(self):
        for record in self:
            record.ingresos = record.posible_ingreso

    @api.depends('ingresos','costes')
    def producto_beneficios(self):
        for record in self:
            record.beneficios = record.ingresos - record.costes

    # Actualiza el Stock clicando sobre el boton Actualizar Stock
    def actualizar_stock(self):
        for recordproducto in self.env['moracorp.ventas'].search([]):
            recordproducto.actualizoRegistrosVentas()
