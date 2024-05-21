from odoo.tests.common import TransactionCase

class TestHrHolidays(TransactionCase):

    def setUp(self):
        super(TestHrHolidays, self).setUp()
        self.allocation = self.env['hr.leave.allocation'].create({
            'name': 'Initial Title',
            'holiday_status_id': self.env.ref('hr_holidays.holiday_status_cl').id,
            'employee_id': self.env.ref('base.user_demo').employee_ids.id,
        })

    def test_title_retain_after_update(self):
        self.allocation.write({'number_of_days': 5})
        self.assertEqual(self.allocation.name, 'Initial Title', "The title should retain the user input after updating other fields.")

    def test_auto_generate_title(self):
        allocation = self.env['hr.leave.allocation'].create({
            'holiday_status_id': self.env.ref('hr_holidays.holiday_status_cl').id,
            'employee_id': self.env.ref('base.user_demo').employee_ids.id,
        })
        self.assertTrue(allocation.name, "The title should be auto-generated if not set by the user.")

