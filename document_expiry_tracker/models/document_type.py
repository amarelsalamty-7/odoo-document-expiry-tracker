from odoo import models , fields 
class DocumentType(models.Model):
    _name = 'document.type'
    _description = 'Document Type'

    name = fields.Char(string='Document Type', required=True)
    description = fields.Text(string='Description')
    active = fields.Boolean(default=True)