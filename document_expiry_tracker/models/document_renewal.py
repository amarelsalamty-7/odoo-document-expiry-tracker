
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class DocumentRenewal(models.Model):
    _name = 'document.renewal'
    _description = 'Document Renewal'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _order = 'request_date desc'

    name = fields.Char(
        string='Renewal Reference',
        required=True,
        default='New',
        tracking=True
    )

    document_id = fields.Many2one(
        'document.tracker',
        string='Document',
        required=True,
        tracking=True
    )

    request_date = fields.Date(
        string='Request Date',
        default=fields.Date.today,
        required=True
    )

    old_expiry_date = fields.Date(
        string='Current Expiry Date',
        readonly=True
    )

    new_expiry_date = fields.Date(
        string='New Expiry Date',
        required=True,
        tracking=True
    )

    responsible_id = fields.Many2one(
        'res.users',
        string='Responsible User',
        default=lambda self: self.env.user,
        tracking=True
    )

    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('waiting_approval', 'Waiting Approval'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True)

    notes = fields.Text(string='Notes')

    # Generate Renewal Reference automatically
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:

            if not vals.get('name') or vals.get('name') == 'New':
                vals['name'] = (
                    self.env['ir.sequence'].next_by_code(
                        'document.renewal'
                    ) or 'New'
                )

            if vals.get('document_id') and not vals.get('old_expiry_date'):
                document = self.env['document.tracker'].browse(
                    vals['document_id']
                )
                vals['old_expiry_date'] = document.expiry_date

        return super().create(vals_list)

    # Validate renewal dates
    @api.constrains('old_expiry_date', 'new_expiry_date')
    def _check_renewal_dates(self):
        for record in self:
            if (
                record.old_expiry_date
                and record.new_expiry_date
                and record.new_expiry_date <= record.old_expiry_date
            ):
                raise ValidationError(
                    'New Expiry Date must be after Current Expiry Date.'
                )

    # Start renewal process
    def action_start(self):
        for record in self:
            if record.state != 'draft':
                raise ValidationError(
                    'Only draft requests can be started.'
                )

            record.state = 'in_progress'

    # Submit for approval
    def action_submit(self):
        for record in self:
            if record.state != 'in_progress':
                raise ValidationError(
                    'Only in-progress requests can be submitted for approval.'
                )

            record.state = 'waiting_approval'

    # Complete renewal
    def action_complete(self):
        for record in self:

            if record.state != 'waiting_approval':
                raise ValidationError(
                    'Only requests waiting for approval can be completed.'
                )

            # Check whether the original document expiry date changed
            if record.document_id.expiry_date != record.old_expiry_date:
                raise ValidationError(
                    'The document expiry date has changed since this '
                    'renewal request was created. Please review the request.'
                )

            # Create renewal history
            record.env['document.renewal.history'].sudo().create({
                'renewal_id': record.id,
                'document_id': record.document_id.id,
                'old_expiry_date': record.old_expiry_date,
                'new_expiry_date': record.new_expiry_date,
                'renewed_by': record.env.user.id,
                'notes': record.notes,
            })

            # Update document expiry date
            record.document_id.write({
                'expiry_date': record.new_expiry_date
            })

            # Update request status
            record.state = 'completed'

    # Cancel renewal
    def action_cancel(self):
        for record in self:
            if record.state in ('completed', 'cancelled'):
                raise ValidationError(
                    'Completed or already cancelled requests cannot be cancelled.'
                )

            record.state = 'cancelled'

    # Prevent duplicate open renewal requests
    @api.constrains('document_id', 'state')
    def _check_duplicate_open_renewal(self):
        for record in self:

            if not record.document_id:
                continue

            if record.state in (
                'draft',
                'in_progress',
                'waiting_approval'
            ):
                duplicate = self.search_count([
                    ('id', '!=', record.id),
                    ('document_id', '=', record.document_id.id),
                    ('state', 'in', [
                        'draft',
                        'in_progress',
                        'waiting_approval'
                    ])
                ])

                if duplicate:
                    raise ValidationError(
                        'An open renewal request already exists '
                        'for this document.'
                    )
