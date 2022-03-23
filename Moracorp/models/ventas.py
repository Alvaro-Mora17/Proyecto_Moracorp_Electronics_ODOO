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
    productos = fields.Many2many("moracorp.productos")
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
                record.precio_venta += producto.precio_iva

    '''
    Funcion para actualizar las ventas registradas
    '''
    def actualizoRegistrosVentas(self):
        #Recorremos partidos y equipos
        for recordproducto in self.env['moracorp.productos'].search([]):
            #Como recalculamos todo, ponemos de cada equipo todo a cero
            recordproducto.posible_venta = 0
            recordproducto.posible_ingreso = 0
            for recordventas in self.env['moracorp.ventas'].search([]):
                for producto in recordventas.productos:
                    if recordproducto.id == producto.id:
                        if recordproducto.cantidad <= 0:
                            raise models.ValidationError('Error no puede comprar ' + producto.nombre + ' porque no hay stock de ese producto.')
                        else:
                            recordproducto.posible_venta += 1
                            recordproducto.posible_ingreso += producto.precio
                            break

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