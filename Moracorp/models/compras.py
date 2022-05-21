# -*- coding: utf-8 -*-

from odoo import models, fields, api

# Definimos el modelo de datos
class Compras(models.Model):
    # Nombre y descripcion del modelo de datos
    _name = 'moracorp.compras'
    _description = 'Modelo de Compras'

    '''Indicamos que cuando se necesite un nombre, se usara el atributo n_transaccion'''
    _rec_name="n_transaccion"

    # Elementos de cada fila del modelo de datos
    id = fields.Integer()
    n_transaccion = fields.Char(string ="Nº de Transaccion")
    proveedor = fields.Many2one('moracorp.proveedores',string ="Nombre del Proveedor")
    fecha_compra = fields.Date(string = "Fecha de Compra")
    fecha_entrega = fields.Date(string = "Fecha de Entrega")
    producto = fields.Many2one("moracorp.productos")
    cantidad = fields.Integer()
    precio_unidad = fields.Float(string= "Precio por Unidad sin IVA")
    porcentaje_iva = fields.Float(string = "Porcentaje de IVA")
    precio_iva = fields.Float(string= "Precio por Unidad con IVA",compute="agregar_iva", store=True)
    precio_total = fields.Float(string = "Precio Total de la Compra",compute="total_compra", store=True)

    # Aplicamos una restriccion sobre el campo numero de transaccion para que sea unico
    _sql_constraints = [
        ('n_transaccion_uniq', 'UNIQUE (n_transaccion)', 'El Número de Transacción debe ser único.')
    ]

    # Saca el precio de la unidad con iva dependiendo del precio sin iva y el porcentaje de iva
    @api.depends('precio_unidad','porcentaje_iva')
    def agregar_iva(self):
        for record in self:
            record.precio_iva = record.precio_unidad + (record.precio_unidad * (record.porcentaje_iva / 100))

    # Saca el precio total de la compra dependiendo del precio de la unidad con el iva incluido y la cantidad
    @api.depends('precio_iva','cantidad')
    def total_compra(self):
        for record in self:
            record.precio_total = record.precio_iva * float(record.cantidad)

    # Aplicamos una restriccion sobre el campo fecha_entrega para que la fecha de entrega sea posterior a la fecha de compra
    @api.constrains('fecha_entrega')
    def check_fecha_entrega(self):
        for record in self:
            if record.fecha_entrega and record.fecha_entrega < record.fecha_compra:
                raise models.ValidationError('La Fecha de Entrega no debe ser anterior a la Fecha de Compra.')

    # Aplicamos una restriccion sobre el campo fecha_compra para que la fecha de compra sea anterior a la fecha de entrega
    @api.constrains('fecha_compra')
    def check_fecha_compra(self):
        for record in self:
            if record.fecha_compra and record.fecha_compra > record.fecha_entrega:
                raise models.ValidationError('La Fecha de Compra no debe ser posterior a la Fecha de Entrega.')
    
    # Aplicamos una restriccion sobre el campo cantidad para que cuando se haga una compra al menos se compre un producto
    @api.constrains('cantidad')
    def check_cantidad_comprada(self):
        for record in self:
            if record.cantidad and record.cantidad < 0 or record.cantidad == 0:
                raise models.ValidationError('La cantidad comprada no debe ser inferior o igual a cero.')

    '''
    Funcion para actualizar las compras registradas
    '''
    def actualizoRegistrosCompras(self):
        # Recorremos productos y compras
        for recordproducto in self.env['moracorp.productos'].search([]):
            # Recalculamos las compras y los costes
            recordproducto.posible_compra = 0
            recordproducto.posible_coste = 0
            for recordcompras in self.env['moracorp.compras'].search([]):
                    if recordproducto.id == recordcompras.producto.id:
                        recordproducto.posible_compra += recordcompras.cantidad
                        recordproducto.posible_coste += recordcompras.precio_total 
   
    # Sobreescribo el metodo crear
    @api.model
    def create(self, values):
        # Hago lo normal del metodo create
        result = super().create(values)
        # Añado esto: llamo a la funcion que actualiza el registro de compras
        self.actualizoRegistrosCompras()
        # Hago lo normal del metodo create
        return result
    
    # Sobreescribo el metodo editar
    def write(self,values):
        result = super(Compras,self).write(values)
        # Añado esto: llamo a la funcion que actualiza el registro de compras
        self.actualizoRegistrosCompras()
        # Hago lo normal del metodo editar
        return result
    
    # Sobreescribo el metodo eliminar
    def unlink(self):
        result = super(Compras,self).unlink()
        # Añado esto: llamo a la funcion que actualiza el registro de compras
        self.actualizoRegistrosCompras()
        return result