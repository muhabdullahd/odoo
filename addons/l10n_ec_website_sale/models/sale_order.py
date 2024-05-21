# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _create_invoices(self, grouped=False, final=False, date=None):
        """ Create invoice(s) for the given Sales Order(s).

        :param bool grouped: if True, invoices are grouped by SO id.
            If False, invoices are grouped by keys returned by :meth:`_get_invoice_grouping_keys`
        :param bool final: if True, refunds will be generated if necessary
        :param date: unused parameter
        :returns: created invoices
        :rtype: `account.move` recordset
        :raises: UserError if one of the orders has no invoiceable lines.
        """
        moves = super()._create_invoices(grouped=grouped, final=final, date=date)
        for move in moves:
            lines_to_remove = move.invoice_line_ids.filtered(lambda l: l.price_unit == 0 and not l.is_downpayment)
            if lines_to_remove:
                _logger.info(f"Removing extra invoice lines with zero value: {lines_to_remove}")
                move.invoice_line_ids -= lines_to_remove
            if move.transaction_ids:
                sri_payment_methods = move.transaction_ids.mapped('payment_method_id.l10n_ec_sri_payment_id')
                if len(sri_payment_methods) == 1:
                    move.l10n_ec_sri_payment_id = sri_payment_methods
        return moves
