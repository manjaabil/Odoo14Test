from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Material(models.Model):
    _name = 'material.registration'
    _description = 'Material Registration'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    material_code = fields.Char(string='Material Code', required=True, tracking=True)
    material_name = fields.Char(string='Material Name', required=True, tracking=True)
    material_type = fields.Selection([
        ('fabric', 'Fabric'),
        ('jeans', 'Jeans'),
        ('cotton', 'Cotton')
    ], string='Material Type', required=True, tracking=True)
    buy_price = fields.Float(string='Material Buy Price', required=True, tracking=True)
    supplier_id = fields.Many2one('res.partner', string='Related Supplier', 
                                 required=True, tracking=True,
                                 domain=[('supplier_rank', '>', 0)])

    _sql_constraints = [
        ('unique_material_code', 'unique(material_code)', 
         'Material Code must be unique!')
    ]

    @api.constrains('buy_price')
    def _check_buy_price(self):
        for record in self:
            if record.buy_price < 100:
                raise ValidationError('Material Buy Price cannot be less than 100!')