# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SalesPersonReport(models.TransientModel):
    _name = 'create.reports'

    person_ids = fields.Many2many('res.users', string="Sales Person")
    person_date = fields.Date(string="Date")

    def create_reports(self):
        lis = []
        for rec in self.person_ids:
            lis.append(rec.name)
        data = {
            'model': 'create.reports',
            'form': self.read()[0],
            'model_id': self.id,
            'person_id': self.person_ids,
            'person_date': self.person_date,
            'person_name': lis

        }
        return self.env.ref('sale_detail_report.sales_person_record_id').report_action(self, data=data)
