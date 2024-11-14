from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestMaterial(TransactionCase):
    def setUp(self):
        super(TestMaterial, self).setUp()
        self.supplier = self.env['res.partner'].create({
            'name': 'Test Supplier',
            'supplier_rank': 1,
        })
        self.material_data = {
            'material_code': 'TEST001',
            'material_name': 'Test Material',
            'material_type': 'fabric',
            'buy_price': 150.0,
            'supplier_id': self.supplier.id,
        }

    def test_create_material(self):
        material = self.env['material.registration'].create(self.material_data)
        self.assertTrue(material.id)
        self.assertEqual(material.material_code, 'TEST001')

    def test_buy_price_constraint(self):
        self.material_data['buy_price'] = 50.0
        with self.assertRaises(ValidationError):
            self.env['material.registration'].create(self.material_data)

    def test_update_material(self):
        material = self.env['material.registration'].create(self.material_data)
        material.write({'material_name': 'Updated Material'})
        self.assertEqual(material.material_name, 'Updated Material')

    def test_delete_material(self):
        material = self.env['material.registration'].create(self.material_data)
        material_id = material.id
        material.unlink()
        self.assertFalse(
            self.env['material.registration'].search([('id', '=', material_id)])
        )