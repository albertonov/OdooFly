# -*- coding: utf-8 -*-

from openerp import models, fields, api, exceptions
from openerp.exceptions import ValidationError


# class odoofly(models.Model):
#     _name = 'odoofly.odoofly'

#     name = fields.Char()


class avion(models.Model):
    _name = 'odoofly.avion'
    name = fields.Char(required=True)
    numeroAsientos = fields.Integer(required=True)
    modelo = fields.Char(required=True)
    trayectos_ids = fields.One2many(
        'odoofly.trayecto', 'avion_id', string="Trayectos")


class aeropuerto(models.Model):
    _name = 'odoofly.aeropuerto'
    name = fields.Char(required=True)
    pais = fields.Many2one('res.country', string="Pais")


class trayecto(models.Model):
    _name = 'odoofly.trayecto'

    name = fields.Char(required=True)
    fecha_salida =  fields.Date(required=True)
    fecha_llegada=  fields.Date(required=True)
    hora_salida = fields.Char(required = True)
    hora_llegada= fields.Char(required = True)

    origen = fields.Many2one('odoofly.aeropuerto', ondelete='cascade', string="Aeropuerto Origen", required=True)   
    destino = fields.Many2one('odoofly.aeropuerto', ondelete='cascade', string="Aeropuerto Destino", required=True)

    pasajeros = fields.Many2many('res.partner', string="Pasajeros", domain=[('is_company','=',False)])

    avion_id = fields.Many2one('odoofly.avion', ondelete='cascade', string="Avion", required=True)

    asientos_disponibles = fields.Integer(string="Asientos disponibles", compute='_calcular_asientos_disponbles')



    @api.depends('avion_id', 'pasajeros')
    def _calcular_asientos_disponbles(self):
                self.asientos_disponibles =  (self.avion_id.numeroAsientos - len(self.pasajeros))


#    @api.onchange('fecha_salida', 'fecha_llegada')
#    def _comprobe_valid_date(self):
#
#        if self.fecha_llegada < self.fecha_salida and self.fecha_salida is not None:
#            return {
#                'warning': {
#                    'title': "Error en las fechas",
#                    'message': "La Fecha de llegada no puede ser anterior a la fecha de salida",
#                },
#            }

    
    @api.constrains('fecha_salida', 'fecha_llegada')
    def _verify_valid_date(self):
                if self.fecha_llegada < self.fecha_salida:
                    raise ValidationError("La Fecha de llegada no puede ser anterior a la fecha de salida")

    @api.constrains('origen','salida')
    def _verify_valid_airports(self):
                if self.origen == self.destino:
                    raise ValidationError("No se puede realizar un trayecto entre dos aeropuertos iguales")


    
    @api.constrains('avion_id', 'pasajeros', 'asientos_disponibles')
    def _verify_valid_asientos(self):
                if self.asientos_disponibles < 0:
                    raise ValidationError("LIMITE DE ASIENTOS ALCANZADO")