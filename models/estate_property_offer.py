from odoo import models, fields, api 
from odoo.exceptions import UserError
from datetime import date
from dateutil.relativedelta import relativedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offers"
    _order = 'price desc'

    price = fields.Float("Price", required=True) 
    status = fields.Selection(selection=[("accepted", "Accepted"), ("refused", "Refused"), ("pending","Pending")], copy=False, required=True)
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(string='Validity (Days)', default=7)
    date_deadline = fields.Date(string='Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline', store=True)
    type_id = fields.Many2one(related="property_id.estate_property_type_id", required = True )

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for offer in self:
            offer.date_deadline = date.today() + relativedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline and record.create_date:
                create_date = record.create_date.date()
                delta = record.date_deadline - create_date
                record.validity = delta.days
            else:
                record.validity = 7  # Fallback to default if create_date is not set


    
    def action_accept(self):
        self.ensure_one()
        if "accepted" in self.property_id.offer_ids.mapped('status'):
            raise UserError('Offer already accepted')
        self.status = "accepted"
        self.property_id.selling_price = self.price
    

        self.property_id.action_sold()  # Set property state to sold
        self.partner_id = self.partner_id
        

        
    

    def action_reject(self):
        self.ensure_one()
        if self.status == "refused":
            raise UserError('This offer has already been refused.')
        
        if "refused" in self.property_id.offer_ids.mapped('status'):
            raise UserError('There is already a refused offer for this property.')
        
        self.status = "refused"
        self.property_id.selling_price = 0
