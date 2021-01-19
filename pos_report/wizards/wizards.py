# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools import date_utils, base64
import datetime
import json
import io
from odoo import _

try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter


class PosExcelDetails(models.TransientModel):
    _inherit = 'pos.details.wizard'

    def create_excel(self):
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
        company_logo = user_obj.company_id.logo
        img_data = base64.b64decode(company_logo)
        image = io.BytesIO(img_data)

        end_date = data['end_date']
        start_date = data['start_date']

        domain = [('state', 'in', ['paid', 'invoiced', 'done']),
                  ('date_order', '>=', start_date),
                  ('date_order', '<=', end_date)]

        orders = self.env['pos.order'].search(domain)
        user_currency = self.env.company.currency_id

        total = 0.0
        products_sold = {}
        taxes = {}
        for order in orders:
            if user_currency != order.pricelist_id.currency_id:
                total += order.pricelist_id.currency_id._convert(
                    order.amount_total, user_currency, order.company_id, order.date_order or fields.Date.today())
            else:
                total += order.amount_total
            currency = order.session_id.currency_id

            for line in order.lines:
                key = (line.product_id, line.price_unit, line.discount)
                products_sold.setdefault(key, 0.0)
                products_sold[key] += line.qty

                if line.tax_ids_after_fiscal_position:
                    line_taxes = line.tax_ids_after_fiscal_position.compute_all(
                        line.price_unit * (1 - (line.discount or 0.0) / 100.0), currency, line.qty,
                        product=line.product_id, partner=line.order_id.partner_id or False)
                    for tax in line_taxes['taxes']:
                        taxes.setdefault(tax['id'], {'name': tax['name'], 'tax_amount': 0.0, 'base_amount': 0.0})
                        taxes[tax['id']]['tax_amount'] += tax['amount']
                        taxes[tax['id']]['base_amount'] += tax['base']
                else:
                    taxes.setdefault(0, {'name': _('No Taxes'), 'tax_amount': 0.0, 'base_amount': 0.0})
                    taxes[0]['base_amount'] += line.price_subtotal_incl
        taxes_list = list(taxes.values())

        query = """select full_product_name,qty,price_unit,date(date_order) as order_date,amount_tax
                from pos_order as po 
               join pos_order_line as pol on pol.order_id =  po.id 
                """

        if data['start_date']:
            query += (" where date(date_order) >= '%s'" % (data['start_date']))
        if data['end_date']:
            query += (" and date(date_order) <= '%s'" % (data['end_date']))

        self._cr.execute(query)
        record = self._cr.dictfetchall()
        query = """ select sum(amount) as total from pos_payment"""
        if data['start_date']:
            query += (" where date(payment_date) >= '%s'" % (data['start_date']))
        if data['end_date']:
            query += (" and date(payment_date) <= '%s'" % (data['end_date']))
        self._cr.execute(query)
        values = self._cr.dictfetchall()
        query = """ select sum(amount) as total,ppm.name as name from pos_payment as pp
                           join pos_payment_method as ppm on pp.payment_method_id = ppm.id"""
        if data['start_date']:
            query += (" where date(payment_date) >= '%s'" % (data['start_date']))
        if data['end_date']:
            query += (" and date(payment_date) <= '%s'" % (data['end_date']))
        query += """group by ppm.name"""
        self._cr.execute(query)
        payment = self._cr.dictfetchall()
        sheet = workbook.add_worksheet()
        format1 = workbook.add_format({'font_size': 22, 'bg_color': '#D3D3D3'})
        format1.set_bold()
        format1.set_align('center')

        format2 = workbook.add_format({'font_size': 9, 'bg_color': '#D3D3D3'})
        format2.set_bold()
        format2.set_text_wrap()
        format2.set_border()

        format3 = workbook.add_format({'font_size': 9, 'bg_color': '#FFFFFF'})
        format3.set_border()

        format4 = workbook.add_format({'font_size': 9, 'bg_color': '#FFFFFF'})
        format4.set_align('center')

        format5 = workbook.add_format({'font_size': 12, 'bg_color': '#D3D3D3'})
        format5.set_bold()
        format5.set_align('center')

        date_format = workbook.add_format({'num_format': 'dd/mm/yy', 'align': 'left', 'font_size': '10px'})
        date_format.set_border()
        date_format.set_align("center")

        sheet.merge_range(6, 7, 6, 11, "(" + start_date + " - " + end_date + ")", date_format)

        sheet.merge_range('A1:C1', user_obj.company_id.name, format3)
        sheet.merge_range('A2:D2', user_obj.company_id.street, format3)
        sheet.merge_range('A3:B3', user_obj.company_id.city, format3)
        sheet.merge_range('C3', user_obj.company_id.zip, format3)
        sheet.merge_range('A4:B4', user_obj.company_id.state_id.name, format3)
        sheet.merge_range('A5:B5', user_obj.company_id.country_id.name, format3)
        sheet.insert_image('F1', company_logo, {'image_data': image, 'x_scale': 0.4, 'y_scale': 0.4})

        sheet.merge_range(4, 6, 5, 12, "SALES DETAILS", format1)
        sheet.merge_range(9, 0, 10, 5, "PRODUCTS", format5)
        sheet.merge_range(12, 0, 12, 3, "PRODUCT ", format2)
        sheet.merge_range(12, 4, 12, 5, "QUANTITY", format2)
        sheet.merge_range(12, 6, 12, 7, "UNIT PRICE", format2)
        sheet.merge_range(12, 8, 12, 9, "ORDER DATE", format2)

        column_number = 0
        row_number = 13

        for rec in record:
            sheet.merge_range(row_number, column_number, row_number, column_number + 3, rec['full_product_name'],
                              format3)

            sheet.merge_range(row_number, column_number + 4, row_number, column_number + 5, rec['qty'],
                              format3)
            sheet.merge_range(row_number, column_number + 6, row_number, column_number + 7, rec['price_unit'],
                              format3)
            sheet.merge_range(row_number, column_number + 8, row_number, column_number + 9, rec['order_date'],
                              date_format)
            row_number += 1
        row_number += 1
        column_number = 0
        sheet.merge_range(row_number + 1, column_number, row_number, column_number + 5, "PAYMENTS", format5)
        sheet.merge_range(row_number + 3, column_number, row_number + 3, column_number + 1, "NAME", format2)
        sheet.merge_range(row_number + 3, column_number + 2, row_number + 3, column_number + 3, "TOTAL", format2)
        column_number = 0
        for pay in payment:
            sheet.merge_range(row_number + 4, column_number, row_number + 4, column_number + 1, pay['name'], format3)
            sheet.merge_range(row_number + 4, column_number + 2, row_number + 4, column_number + 3, pay['total'],
                              format3)
            row_number += 1
        row_number += 1
        column_number = 0
        sheet.merge_range(row_number + 4, column_number, row_number + 4, column_number + 5, "TAXES", format5)
        sheet.merge_range(row_number + 6, column_number, row_number + 6, column_number + 1, "NAME", format2)
        sheet.merge_range(row_number + 6, column_number + 2, row_number + 6, column_number + 3, "TAX AMOUNT", format2)
        sheet.merge_range(row_number + 6, column_number + 4, row_number + 6, column_number + 5, "BASE AMOUNT", format2)
        column_number = 0
        for tax in taxes_list:
            sheet.merge_range(row_number + 7, column_number, row_number + 7, column_number + 1, tax['name'],
                              format3)
            sheet.merge_range(row_number + 7, column_number + 2, row_number + 7, column_number + 3,
                              tax['tax_amount'], format3)
            sheet.merge_range(row_number + 7, column_number + 4, row_number + 7, column_number + 5, tax['base_amount'],
                              format3)
            row_number += 1
        print(row_number)
        column_number = 0
        for val in values:
            sheet.merge_range(row_number + 8, column_number, row_number + 8, column_number + 1, "TOTAL", format2)
            sheet.merge_range(row_number + 8, column_number + 2, row_number + 8, column_number + 3, val['total'],
                              format3)
        workbook.close()

        output.seek(0)

        response.stream.write(output.read())

        output.close()
