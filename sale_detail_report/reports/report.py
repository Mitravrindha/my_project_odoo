from odoo import models, fields, api


class SalePersonReport(models.Model):
    _name = 'report.sale_detail_report.report_sales_person'

    @api.model
    def _get_report_values(self, docids, data):
        query = """SELECT s_o.name as s_o_name,s_o_l.name as s_o_l_name,s_o.user_id,date(s_o.date_order) as date_order,
        s_o_l.product_uom_qty,
        s_o_l.price_unit
        ,s_o_l.price_subtotal,r_p.name as s_p_name,r_u.login,r.name as customer_name FROM sale_order as s_o
        JOIN sale_order_line as s_o_l ON s_o.id = s_o_l.order_id
        JOIN res_users as r_u ON s_o.user_id = r_u.id
        left JOIN res_partner as r_p ON r_u.partner_id = r_p.id
        join res_partner as r on s_o.partner_id = r.id """

        lis = data['form']['person_ids']
        tup = str(tuple(lis)).replace(',)', ')')

        if data['form']['person_ids']:
            query += (" where s_o.user_id in {}".format(tup))
        if data['form']['person_date']:
            query += ("and  date(s_o.date_order) ='%s'" % (data['person_date']))
        query += "order by s_p_name"
        self._cr.execute(query)
        record = self._cr.dictfetchall()

        query = """select r_p.name as name from res_users as r_u
                    join res_partner as r_p ON r_u.partner_id = r_p.id
                    where r_u.active = 'True'"""
        if data['form']['person_ids']:
            query += (" and r_u.id in {}".format(tup))
        self._cr.execute(query)
        values = self._cr.dictfetchall()
        print(values)


        return {
            'docs': record,
            'val': values,
            'person_date': data['person_date'],
        }
