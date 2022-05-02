# -*- coding: utf-8 -*-

from odoo import models, fields, api

#Definimos el modelo de datos
class Ventas(models.Model):
    #Nombre y descripcion del modelo de datos
    _name = 'moracorp.ventas'
    _description = 'Modelo de Ventas'
    #Como no tenemos un atributo "name" en nuestro modelo, indicamos que cuando
    #se necesite un nombre, se usara el atributo tarea
    _rec_name="n_transaccion"

    #Elementos de cada fila del modelo de datos
    id = fields.Integer()
    n_transaccion = fields.Char(string ="Nº de Transaccion")
    fecha_compra = fields.Date(string = "Fecha de Venta")
    cliente = fields.Many2one('moracorp.clientes')
    productos = fields.Many2many("moracorp.transaccion_venta")
    precio_venta = fields.Float(string = "Precio Total de la Venta",compute="total_venta", store=True)

    # Aplicamos una restriccion sobre el campo numero de transaccion para que sea unico
    _sql_constraints = [
        ('n_transaccion_uniq', 'UNIQUE (n_transaccion)', 'El Número de Transacción debe ser único.')
    ]

    # Saca el precio total de la venta dependiendo de los productos que haya en el campo productos   
    @api.depends('productos')
    def total_venta(self):
        for record in self:
            record.precio_venta = 0
            for producto in self.productos:
                record.precio_venta += producto.precio_iva * producto.cantidad_vendida

    '''
    Funcion para actualizar las ventas registradas
    '''
    def actualizoRegistrosVentas(self):
        #Recorremos productos y ventas
        for recordproducto in self.env['moracorp.productos'].search([]):
            #Recalculamos las ventas y los ingresos
            recordproducto.posible_venta = 0
            recordproducto.posible_ingreso = 0
            for recordventas in self.env['moracorp.ventas'].search([]):
                '''Recorremos el campo productos que es el encargado de relacionar mediante una 
                relacion Many2many Ventas con el modelo heredero de productos denominado Transaccion Venta'''
                for producto in recordventas.productos:
                    if recordproducto.nombre == producto.nombre:
                        if recordproducto.cantidad - producto.cantidad_vendida < 0:
                            raise models.ValidationError('Error no puede comprar ' + producto.nombre + ' porque no hay stock de ese producto.')
                        else:
                            recordproducto.posible_venta += producto.cantidad_vendida
                            recordproducto.posible_ingreso += producto.precio * producto.cantidad_vendida

    #Sobreescribo el metodo crear
    @api.model
    def create(self, values):
        #hago lo normal del metodo create
        result = super().create(values)
        #Añado esto: llamo a la funcion que actualiza el registro de venta
        self.actualizoRegistrosVentas()
        #hago lo normal del metodo create
        return result
    
    #Sobreescribo el metodo editar
    def write(self,values):
        result = super(Ventas,self).write(values)
        #Añado esto: llamo a la funcion que actualiza el registro de venta
        self.actualizoRegistrosVentas()
        #hago lo normal del metodo editar
        return result
    
    #Sobreescribo el metodo eliminar
    def unlink(self):
        result = super(Ventas,self).unlink()
        #Añado esto: llamo a la funcion que actualiza el registro de venta
        self.actualizoRegistrosVentas()
        return result