from odoo import models, fields, api
from odoo.exceptions import ValidationError


class DocumentTracker(models.Model):
    _name = 'document.tracker'
    _description = 'Document Tracker'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _order = 'expiry_date asc'

    # Basic Information
    name = fields.Char(
        string='Document Name',
        required=True,
        tracking=True
    )

    document_number = fields.Char(
        string='Document Number',
        tracking=True
    )

    document_type_id = fields.Many2one(
        'document.type',
        string='Document Type',
        required=True,
        tracking=True
    )

    # Related Information
    related_party_id = fields.Many2one(
        'res.partner',
        string='Related Employee / Entity'
    )

    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        required=True
    )

    responsible_id = fields.Many2one(
        'res.users',
        string='Responsible User',
        default=lambda self: self.env.user,
        tracking=True
    )

    # Dates
    issue_date = fields.Date(string='Issue Date')

    expiry_date = fields.Date(
        string='Expiry Date',
        required=True,
        tracking=True
    )

    # Attachment
    attachment = fields.Binary(
        string='Document Attachment',
        attachment=True
    )

    attachment_filename = fields.Char(string='File Name')

    # Automatic Status
    # Stored so they can be used in Group By, Graph and Pivot views.
    # They are refreshed daily by the cron (_cron_check_document_expiry).
    status = fields.Selection(
        [
            ('draft', 'Draft'),
            ('active', 'Active'),
            ('expiring', 'Expiring Soon'),
            ('expired', 'Expired'),
        ],
        string='Status',
        compute='_compute_status',
        store=True
    )

    days_remaining = fields.Integer(
        string='Days Remaining',
        compute='_compute_status',
        store=True
    )

    # Renewal History
    renewal_history_ids = fields.One2many(
        'document.renewal.history',
        'document_id',
        string='Renewal History'
    )

    renewal_history_count = fields.Integer(
        string='Renewal History Count',
        compute='_compute_renewal_history_count'
    )

    @api.depends('renewal_history_ids')
    def _compute_renewal_history_count(self):
        for record in self:
            record.renewal_history_count = len(
                record.renewal_history_ids
            )

    def action_view_renewal_history(self):
        self.ensure_one()

        return {
            'type': 'ir.actions.act_window',
            'name': 'Renewal History',
            'res_model': 'document.renewal.history',
            'view_mode': 'list,form',
            'domain': [('document_id', '=', self.id)],
            'context': {
                'default_document_id': self.id,
            },
        }

    # Compute Document Status
    @api.depends('expiry_date')
    def _compute_status(self):
        today = fields.Date.today()

        for record in self:
            if not record.expiry_date:
                record.status = 'draft'
                record.days_remaining = 0
                continue

            remaining = (record.expiry_date - today).days
            record.days_remaining = remaining

            if remaining < 0:
                record.status = 'expired'
            elif remaining <= 30:
                record.status = 'expiring'
            else:
                record.status = 'active'

    # Date Validation
    @api.constrains('issue_date', 'expiry_date')
    def _check_dates(self):
        for record in self:
            if (
                record.issue_date
                and record.expiry_date
                and record.expiry_date < record.issue_date
            ):
                raise ValidationError(
                    'Expiry Date cannot be before Issue Date!'
                )