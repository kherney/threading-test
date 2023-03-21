from odoo import fields, models, api


class Lines(models.Model):
    _name = 'line.test'
    _description = 'nnnn'

    name = fields.Char()
    line = fields.Many2one("account.move.line", )
    dest_id = fields.Many2one("dest.header.test")
