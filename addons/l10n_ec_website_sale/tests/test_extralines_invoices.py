from odoo.tests.common import TransactionCase

class TestSaleOrder(TransactionCase):

    def setUp(self):
        super(TestSaleOrder, self).setUp()
        self.product = self.env['product.product'].create({
            'name': 'Test Product',
            'type': 'service',
        })
        self.sale_order = self.env['sale.order'].create({
            'partner_id': self.env.ref('base.res_partner_1').id,
            'order_line': [(0, 0, {
                'product_id': self.product.id,
                'product_uom_qty': 1,
                'price_unit': 100,
            })]
        })
        self.sale_order.action_confirm()

    def test_no_extra_zero_value_line(self):
        invoice = self.sale_order._create_invoices()
        invoice_line_count = len(invoice.invoice_line_ids)
        # Simulate removing tax and creating another downpayment invoice
        invoice.write({'invoice_line_ids': [(1, line.id, {'tax_ids': [(6, 0, [])]}) for line in invoice.invoice_line_ids]})
        new_invoice = self.sale_order._create_invoices()
        new_invoice_line_count = len(new_invoice.invoice_line_ids)
        self.assertEqual(invoice_line_count, new_invoice_line_count, "There should be no extra zero-value line in downpayment invoices.")

    def test_downpayment_creation(self):
        invoice = self.sale_order._create_invoices()
        self.assertTrue(invoice, "Downpayment invoice should be created successfully.")
        self.assertEqual(len(invoice.invoice_line_ids), 1, "Downpayment invoice should have one line.")
        self.assertEqual(invoice.invoice_line_ids[0].price_unit, 100, "Invoice line price should be 100.")
