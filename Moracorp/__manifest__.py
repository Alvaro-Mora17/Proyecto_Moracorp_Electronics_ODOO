# -*- coding: utf-8 -*-
{
    'name': "Administracion Moracorp",

    'summary': """
    """,

    'description': """
    """,

    'author': "Alvaro Mora Lopez",
    #Indicamos que es una aplicación
    'application': True,

    # En la siguiente URL se indica que categorias pueden usarse
    # https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # Vamos a utilizar la categoria Productivity
    'category': 'Productivity',
    'version': '0.1',

    # Indicamos lista de modulos necesarios para que este funcione correctamente
    # En este ejemplo solo depende del modulo "base"
    'depends': ['base'],
    'qweb': [
        'static/src/xml/qweb.xml',
    ],

    # Esto siempre se carga
    'data': [
        #El primer fichero indica la politica de acceso del modelo
        #Mas información en https://www.odoo.com/documentation/14.0/es/developer/howtos/rdtraining/05_securityintro.html
        'security/ir.model.access.csv',
        #Cargamos las vistas y las plantillas
        'views/productos_view.xml',
        'views/compras_view.xml',
        'views/ventas_view.xml',
        'views/stock_view.xml',
        'views/proveedores_view.xml',
        'views/clientes_view.xml',
        'views/pedidos_view.xml',
        'views/transaccion_venta_view.xml'
    ]
    
}
