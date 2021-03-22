""" Paytrail Payment Gateway integration """
import hashlib
import sys
from datetime import datetime
from werkzeug import urls
from odoo import models, fields, api, _
import logging

from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class PaytrailGateway(models.Model):
    """Adding Payment Acquirer and  payment functions"""
    _inherit = 'payment.acquirer'
    provider = fields.Selection(selection_add=[('paytrail', 'Paytrail')],
                                ondelete={'paytrail': 'set '
                                                      'default'})
    # MERCHANT_ID
    paytrail_merchant_id = fields.Char('Merchant ID',
                                       required_if_provider='Paytrail',
                                       groups='base.group_user')
    # MERCHANT_AUTHENTICATION HASH
    paytrail_merchant_key = fields.Char('Merchant Key',
                                        required_if_provider='Paytrail',
                                        groups='base.group_user')

    @api.model
    def _get_paytrail_urls(self):
        """ Atom URLS """
        return {
            'paytrail_form_url': 'https://payment.paytrail.com/e2'
        }

    def paytrail_get_form_action_url(self):
        """getting the form action url of paytail"""
        return self._get_paytrail_urls()['paytrail_form_url']

    def paytrail_form_generate_values(self, values):
        """Adding Values to the Dict  and to form"""
        self.ensure_one()
        base_url = self.env['ir.config_parameter'].sudo().get_param(
            'web.base.url')
        now = datetime.now()

        paytrail_values = dict(
            MERCHANTAUTHENTICATIONHASH=self.paytrail_merchant_key,
            MERCHANT_ID=self.paytrail_merchant_id,
            URL_SUCCESS=urls.url_join(base_url,
                                      '/payment.paytrail.com/return/'),
            URL_CANCEL=urls.url_join(base_url, '/payment.paytrail.com/cancel/'),
            ORDER_NUMBER=str(values['reference']),
            PARAMS_IN='MERCHANT_ID,URL_SUCCESS,URL_CANCEL,ORDER_NUMBER,PARAMS_IN,PARAMS_OUT,AMOUNT',
            PARAMS_OUT='ORDER_NUMBER,PAYMENT_ID,TIMESTAMP,STATUS',
            AMOUNT=str(values['amount']),
        )
        paytrail_values['AUTHCODE'] = self.generate_checksum_by_str(
            paytrail_values,
            self.paytrail_merchant_key)
        return paytrail_values

    def __get_param_string__(self, params, escape_refund=True):
        """Adding | after each item"""
        params_string = []
        for key in params.keys():
            if ("|" in params[key] or (
                    escape_refund == True and "REFUND" in params[key])):
                # respons_dict = {}
                sys.exit()
            value = params[key]
            if type(value) != list:
                params_string.append('' if value == 'null' else str(value))
            else:
                params_string.append(
                    '' if value == 'null' else str(value)[1:-1])
        return '|'.join(params_string)

    def generate_checksum_by_str(self, param_str, merchant_key, salt=None):
        """Creating Hash using sha256 """
        params_string = self.__get_param_string__(param_str)
        hasher = hashlib.sha256(params_string.encode("UTF-8"))
        hash_string = hasher.hexdigest()
        final_hash = hash_string.upper()
        return final_hash


class PaymentTransaction(models.Model):
    """ PAYMENT TRANSACTION model adding datas to payment trasaction form"""
    _inherit = 'payment.transaction'

    @api.model
    def _paytrail_form_get_tx_from_data(self, data):
        """Getting datas """
        reference = data.get('ORDER_NUMBER')
        if not reference:
            error_msg = _(
                'Paytm: received data with missing reference (%s)') % (
                            reference)
            _logger.info(error_msg)
            raise ValidationError(error_msg)

        txs = self.env['payment.transaction'].search(
            [('reference', '=', reference)])
        if not txs or len(txs) > 1:
            error_msg = 'Paytrail: received data for reference %s' % (reference)
            if not txs:
                error_msg += '; no order found'
            else:
                error_msg += '; multiple order found'
            _logger.info(error_msg)
            raise ValidationError(error_msg)
        return txs[0]

    def _paytrail_form_get_invalid_parameters(self, data):
        invalid_parameters = []
        if self.acquirer_reference and data.get(
                'PAYMENT_ID') != self.acquirer_reference:
            invalid_parameters.append(
                ('ORDER_NUMBER', data.get('ORDER_NUMBER'),
                 self.acquirer_reference))
        return invalid_parameters

    def _paytrail_form_validate(self, data):
        """Writing datas to payment transaction form"""
        status = data.get('STATUS')
        result = self.write({
            'acquirer_reference': data.get('PAYMENT_ID'),
            'date': fields.Datetime.now(),

        })
        if status == 'PAID':
            self._set_transaction_done()
        elif status != 'CANCELLED':
            self._set_transaction_cancel()
        else:
            self._set_transaction_pending()
        return result
