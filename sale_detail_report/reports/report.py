from odoo import models, fields, api


class SalePersonReport(models.Model):
    _name = 'report.sale_detail_report.report_sales_person'
    user_id = fields.Many2one('res.users', 'Salesperson', readonly=True)

    @api.model
    def _get_report_values(self, docids, data):
        query = """SELECT s_o.name as s_o_name,s_o_l.name as s_o_l_name,s_o.user_id,date(s_o.date_order) as date_order,
        s_o_l.product_uom_qty,
        s_o_l.price_unit
        ,s_o_l.price_subtotal,r_p.name as s_p_name,r_u.login FROM sale_order as s_o
        JOIN sale_order_line as s_o_l ON s_o.id = s_o_l.order_id
        JOIN res_users as r_u ON s_o.user_id = r_u.id
        JOIN res_partner as r_p ON r_u.partner_id = r_p.id """

        if data['form']['person_id']:
            query += (" where s_o.user_id = '%s' " % (data['form']['person_id'][0]))
        if data['person_date']:
            query += (" and  date(s_o.date_order) ='%s'" % (data['person_date']))
        if not (data['form']['person_id']):
            print("ooooooo")


        print(query)
        # print(data['form']['person_id'][1])
        self._cr.execute(query)
        record = self._cr.dictfetchall()
        print(record)

        return {
            'docs': record,
            'person_id': data['form']['person_id'][1] if data['form']['person_id'] else None,
            'person_date': data['person_date'],
        }
