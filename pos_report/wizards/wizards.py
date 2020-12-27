# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools import date_utils
import datetime
import json
import io

try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter


class PosExcelDetails(models.TransientModel):
    _inherit = 'pos.details.wizard'

    def create_excel(self):
        print("kite")
        print(self.start_date)
        data = {
            'start_date': self.start_date,
            'end_date': self.end_date,
        }

        return {

            'type': 'ir.actions.report',

            'data': {'model': 'pos.details.wizard',
                     'options': json.dumps(data, default=date_utils.json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Excel Report',
                     },
            'report_type': 'xlsx'
        }

    def get_xlsx_report(self, data, response):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        user_obj = self.env.user

        sheet = workbook.add_worksheet()
        format1 = workbook.add_format({'font_size': 22, 'bg_color': '#D3D3D3'})
        format1.set_bold()
        format1.set_align('center')

        format2 = workbook.add_format({'font_size': 9, 'bg_color': '#D3D3D3'})
        format2.set_bold()
        format2.set_text_wrap()
        format2.set_border()

        format3 = workbook.add_format({'font_size': 9, 'bg_color': '#FFFFFF'})
        format4 = workbook.add_format({'font_size': 9, 'bg_color': '#FFFFFF'})
        format4.set_align('center')

        format5 = workbook.add_format({'font_size': 12, 'bg_color': '#D3D3D3'})
        format5.set_bold()
        format5.set_align('center')

        sheet.merge_range('A1:C1', user_obj.company_id.name, format3)
        sheet.merge_range('A2:D2', user_obj.company_id.street, format3)
        sheet.merge_range('A3:B3', user_obj.company_id.city, format3)
        sheet.merge_range('C3', user_obj.company_id.zip, format3)
        sheet.merge_range('A4:B4', user_obj.company_id.state_id.name, format3)
        sheet.merge_range('A5:B5', user_obj.company_id.country_id.name, format3)

        sheet.merge_range(5, 0, 6, 8, "SALE DETAILS", format1)
        sheet.merge_range(9, 0, 10, 5, "PRODUCTS", format5)
        sheet.merge_range(12, 0, 12, 1, "PRODUCT ", format2)
        sheet.merge_range(12, 2, 12, 3, "QUANTITY", format2)
        sheet.merge_range(12, 4, 12, 5, "UNIT PRICE", format2)

        # query =

        workbook.close()

        output.seek(0)

        response.stream.write(output.read())

        output.close()
