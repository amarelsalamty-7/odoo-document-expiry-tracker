from datetime import timedelta

from odoo import api, fields, models


class DocumentTracker(models.Model):
    _inherit = 'document.tracker'

    @api.model
    def get_dashboard_data(self):
        """Return KPI cards and chart data for the Document Dashboard.

        Every item carries its own model and domain, so the dashboard can
        open the matching list when the user clicks on it.
        """
        today = fields.Date.context_today(self)
        limit = today + timedelta(days=30)
        today_s = fields.Date.to_string(today)
        limit_s = fields.Date.to_string(limit)

        doc_model = 'document.tracker'
        ren_model = 'document.renewal'
        Renewal = self.env[ren_model]

        # Same boundaries as the search filters and the status computation
        status_domains = {
            'active': [('expiry_date', '>', limit_s)],
            'expiring': [
                ('expiry_date', '>=', today_s),
                ('expiry_date', '<=', limit_s),
            ],
            'expired': [('expiry_date', '<', today_s)],
        }

        def doc_item(label, color, domain):
            return {
                'label': label,
                'color': color,
                'model': doc_model,
                'domain': domain,
                'count': self.search_count(domain),
            }

        def ren_item(label, color, domain):
            return {
                'label': label,
                'color': color,
                'model': ren_model,
                'domain': domain,
                'count': Renewal.search_count(domain),
            }

        active = doc_item('Active', 'success', status_domains['active'])
        expiring = doc_item('Expiring Soon', 'warning', status_domains['expiring'])
        expired = doc_item('Expired', 'danger', status_domains['expired'])

        document_kpis = [
            doc_item('Total Documents', 'primary', []),
            active,
            expiring,
            expired,
        ]

        renewal_kpis = [
            ren_item('Total Requests', 'primary', []),
            ren_item('Pending Approval', 'warning',
                     [('state', '=', 'waiting_approval')]),
            ren_item('Completed', 'success', [('state', '=', 'completed')]),
        ]

        # Documents by type (top 10)
        groups = self._read_group([], ['document_type_id'], ['__count'])
        by_type = [
            {
                'label': record.display_name,
                'color': 'primary',
                'model': doc_model,
                'domain': [('document_type_id', '=', record.id)],
                'count': count,
            }
            for record, count in groups
            if record
        ]
        by_type.sort(key=lambda item: -item['count'])

        return {
            'document_kpis': document_kpis,
            'renewal_kpis': renewal_kpis,
            'by_status': [active, expiring, expired],
            'by_type': by_type[:10],
        }