# -*- coding: utf-8 -*-
from openerp import fields, models

class Partner(models.Model):
    _inherit = 'res.partner'

    # Add a new column to the res.partner model, by default partners are not
    # instructors
    

    trayectos_ids = fields.Many2many('odoofly.trayecto',
        string="Historial de vuelos", readonly=True)