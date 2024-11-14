from odoo import http
from odoo.http import request
import json

class MaterialController(http.Controller):
    @http.route('/api/materials', type='http', auth='user', methods=['GET'], csrf=False)
    def get_materials(self, **kwargs):
        domain = []
        if kwargs.get('material_type'):
            domain.append(('material_type', '=', kwargs.get('material_type')))
            
        materials = request.env['material.registration'].search_read(
            domain=domain,
            fields=['material_code', 'material_name', 'material_type', 
                   'buy_price', 'supplier_id']
        )
        return http.Response(
            json.dumps({'status': 'success', 'data': materials}),
            content_type='application/json'
        )

    @http.route('/api/materials', type='json', auth='user', methods=['POST'])
    def create_material(self, **kwargs):
        try:
            material = request.env['material.registration'].create(kwargs)
            return {
                'status': 'success',
                'id': material.id,
                'message': 'Material created successfully'
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }

    @http.route('/api/materials/<int:material_id>', type='json', 
                auth='user', methods=['PUT'])
    def update_material(self, material_id, **kwargs):
        try:
            material = request.env['material.registration'].browse(material_id)
            if not material.exists():
                return {'status': 'error', 'message': 'Material not found'}
            
            material.write(kwargs)
            return {
                'status': 'success',
                'message': 'Material updated successfully'
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }

    @http.route('/api/materials/<int:material_id>', type='http', 
                auth='user', methods=['DELETE'], csrf=False)
    def delete_material(self, material_id):
        try:
            material = request.env['material.registration'].browse(material_id)
            if not material.exists():
                return http.Response(
                    json.dumps({'status': 'error', 'message': 'Material not found'}),
                    content_type='application/json'
                )
            
            material.unlink()
            return http.Response(
                json.dumps({
                    'status': 'success',
                    'message': 'Material deleted successfully'
                }),
                content_type='application/json'
            )
        except Exception as e:
            return http.Response(
                json.dumps({'status': 'error', 'message': str(e)}),
                content_type='application/json'
            )