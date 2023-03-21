from odoo import fields, models, api


class DestHeader(models.Model):
    _name = 'dest.header.test'
    _description = 'jifsd'

    partner_id = fields.Many2one("res.partner")
    ident = fields.Char("str")
    line_ids = fields.One2many("line.test", 'dest_id')
    date = fields.Date("the date")
    header_id = fields.Many2one("header.test")
