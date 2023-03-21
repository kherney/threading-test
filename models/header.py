from odoo import fields, models, api
from odoo import SUPERUSER_ID
from odoo import sql_db

import threading


class Header(models.Model):
    _name = 'header.test'
    _description = 'nnnnn'

    @api.model
    def get_key(self, line):
        return line.partner_id, line.partner_id.id

    def _get_group_key(self):
        groups = {}
        for line in self.line_ids:
            key_group = self.get_key(line)
            if key_group in groups.keys():
                groups[key_group] += line
            else:
                groups.update({key_group: line})
        return groups

    name = fields.Char()
    line_ids = fields.Many2many("account.move.line", relation="move_line_header")
    state = fields.Selection([('draft', 'Draft'), ('done', 'Done')], default='draft')
    dst_ids = fields.One2many("dest.header.test", 'header_id')

    def post_button(self):
        for header in self:
            if not header:
                continue

            header.create_dest()

        self.write({'state': 'done'})

    def create_dest(self):
        groups = self._get_group_key()

        cr = self.env.cr

        for _, values in groups.items():
            th = threading.Thread(target=self._create_dest, args=(cr, values))
            th.start()

        cr.commit()

    def _create_dest(self, cr, lines):
        try:
            with api.Environment.manage():
                # Create a new environment and cursor for each thread
                env = api.Environment(sql_db.db_connect('main_db'), SUPERUSER_ID, {})
                cr = env.cr
                # Create a database savepoint for each thread
                savepoint = cr.savepoint()
                obj = env['dest.header.test'].create({
                    'partner_id': lines.mapped('partner_id')[-1].id,
                    'line_ids': [(0, 0, {'name': self.name, 'line': line.id}) for line in lines],
                    'header_id': self.id,
                })
                # Your code here
                ...

        except Exception as e:
            # Handle exceptions here
            ...
            # Rollback the database to the savepoint in case of exceptions
            cr.rollback()
        finally:
            if not cr.rollback():
                cr.commit()
            # Close the cursor, even in case of exceptions
            pass

        return obj

    def draft_button(self):
        for header in self:
            header.dst_ids.unlink()
        self.write({'state': 'draft'})
