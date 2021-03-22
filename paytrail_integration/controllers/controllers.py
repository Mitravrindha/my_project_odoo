""" Controller For Paytrail gateway. Redirect to the success page"""
import logging
import pprint
import werkzeug
from werkzeug.utils import redirect
from odoo import http
from odoo.http import request


_logger = logging.getLogger(__name__)


class AtomController(http.Controller):
    """Redirecting controller """

    @http.route(['/payment.paytrail.com/return/',
                 '/payment.paytrail.com/cancel/',
                 '/payment.paytrail.com/error/'],
                type='http', methods=['POST', 'GET'],
                auth='public', csrf=False)
    def paytrail_return(self, **post):
        """return function to return  url"""
        print(post)
        _logger.info(
            'Paytrail: entering form_feedback with post data %s',
            pprint.pformat(post))
        if post:
            request.env['payment.transaction'].sudo().form_feedback(post,
                                                                    'paytrail')
        return werkzeug.utils.redirect('/payment/process')
