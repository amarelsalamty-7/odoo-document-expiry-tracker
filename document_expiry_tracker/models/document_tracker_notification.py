from datetime import timedelta

from odoo import api, fields, models, _


class DocumentTracker(models.Model):
    _inherit = 'document.tracker'

    reminder_30_sent = fields.Boolean(
        string='30-Day Reminder Sent', default=False, copy=False, readonly=True
    )
    reminder_7_sent = fields.Boolean(
        string='7-Day Reminder Sent', default=False, copy=False, readonly=True
    )
    expired_notified = fields.Boolean(
        string='Expiry Notification Sent', default=False, copy=False, readonly=True
    )

    def write(self, vals):
        # When the expiry date changes (e.g. after a renewal),
        # reset the flags so reminders start again for the new date.
        if 'expiry_date' in vals:
            vals = dict(
                vals,
                reminder_30_sent=False,
                reminder_7_sent=False,
                expired_notified=False,
            )
        return super().write(vals)

    def _send_expiry_notification(self, subject, body):
        """Post a message to the responsible user (inbox/email)
        and schedule a to-do activity when the mixin is available."""
        self.ensure_one()
        partner_ids = self.responsible_id.partner_id.ids
        self.message_post(
            subject=subject,
            body=body,
            partner_ids=partner_ids,
            message_type='comment',
            subtype_xmlid='mail.mt_comment',
        )
        if self.responsible_id and 'activity_ids' in self._fields:
            self.activity_schedule(
                'mail.mail_activity_data_todo',
                date_deadline=fields.Date.context_today(self),
                summary=subject,
                user_id=self.responsible_id.id,
            )

    @api.model
    def _cron_check_document_expiry(self):
        today = fields.Date.context_today(self)
        in_7_days = today + timedelta(days=7)
        in_30_days = today + timedelta(days=30)

        # 1) Expired documents
        expired = self.search([
            ('expiry_date', '<', today),
            ('expired_notified', '=', False),
        ])
        for rec in expired:
            rec._send_expiry_notification(
                _('Document Expired: %s', rec.name),
                _('The document "%(name)s" expired on %(date)s. '
                  'Please start a renewal request.',
                  name=rec.name, date=rec.expiry_date),
            )
        expired.write({'expired_notified': True})

        # 2) Urgent: 7 days or less remaining
        urgent = self.search([
            ('expiry_date', '>=', today),
            ('expiry_date', '<=', in_7_days),
            ('reminder_7_sent', '=', False),
        ])
        for rec in urgent:
            days_left = (rec.expiry_date - today).days
            rec._send_expiry_notification(
                _('URGENT: Document expires in %s day(s)', days_left),
                _('The document "%(name)s" expires on %(date)s '
                  '(%(days)s day(s) left).',
                  name=rec.name, date=rec.expiry_date, days=days_left),
            )
        urgent.write({'reminder_7_sent': True, 'reminder_30_sent': True})

        # 3) Reminder: between 8 and 30 days remaining
        upcoming = self.search([
            ('expiry_date', '>', in_7_days),
            ('expiry_date', '<=', in_30_days),
            ('reminder_30_sent', '=', False),
        ])
        for rec in upcoming:
            days_left = (rec.expiry_date - today).days
            rec._send_expiry_notification(
                _('Reminder: Document expires in %s days', days_left),
                _('The document "%(name)s" expires on %(date)s '
                  '(%(days)s days left).',
                  name=rec.name, date=rec.expiry_date, days=days_left),
            )
        upcoming.write({'reminder_30_sent': True})