
from odoo import models, fields


class DocumentRenewalHistory(models.Model):
    _name = 'document.renewal.history'
    _description = 'Document Renewal History'
    _order = 'renewal_date desc'

    renewal_id = fields.Many2one(
        'document.renewal',
        string='Renewal Request',
        required=True,
        ondelete='restrict'
    )

    document_id = fields.Many2one(
        'document.tracker',
        string='Document',
        required=True,
        ondelete='restrict'
    )

    old_expiry_date = fields.Date(
        string='Previous Expiry Date',
        required=True
    )

    new_expiry_date = fields.Date(
        string='New Expiry Date',
        required=True
    )

    renewal_date = fields.Datetime(
        string='Renewal Date',
        default=fields.Datetime.now,
        required=True
    )

    renewed_by = fields.Many2one(
        'res.users',
        string='Renewed By',
        default=lambda self: self.env.user,
        required=True
    )

    notes = fields.Text(string='Notes')
