from odoo import models,fields,api, _
from odoo.exceptions import UserError, ValidationError

class EstateProperty(models.Model):
    _name='estate.property'
    _description='Estate Property'
    _sql_constrains= [
        ("positive_expected_price", "CHECK(expected_price >= 0)","Enter a positive amount on Expected Price."),
        ("positive_selling_price", "CHECK(selling_price > 0)", "Selling price must be positive.")
    ]
    _order = 'name desc'

        


    name=fields.Char('Property Name',required=True)
    description= fields.Text('Description')
    postcode= fields.Char("Postcode")
    date_availability= fields.Date("Availability Date",copy=False, required = True)
    expected_price =  fields.Float ("Expected Price", required = True)
    selling_price = fields.Float ("Selling Price",readonly=True,copy=False)
    bedrooms = fields.Integer ("Bedrooms",default=2)
    living_area = fields.Integer ("Living Area")
    facades = fields.Integer ("Facades")
    garage = fields.Boolean ("Garage")
    garden = fields.Boolean ("Garden")
    garden_area = fields.Integer ("Garden Area")
    garage_orientation = fields.Selection(selection=[('north','North'),
                                                     ("south","South"),
                                                     ("west","West"),
                                                     ("east","East")],
                                                     required=True)
    state = fields.Selection (selection=[("new","New"),
                                         ("offer_received","Offer Received"),
                                         ("offer_accepted","Offer Accepted"),
                                         ("cancelled","Cancelled"),
                                         ("sold","Sold"),],
                                         copy=False,
                                         default="new")
    estate_property_type_id = fields.Many2one ("estate.property.type", string="Property Type")
    buyer = fields.Many2one ("res.partner", copy=False)
    salesperson = fields.Many2one ('res.users', string='Salesperson', index=True, tracking=True, default=lambda self: self.env.user)
    offer_ids = fields.One2many ("estate.property.offer", "property_id")
    property_tag_ids = fields.Many2many ("estate.property.tags" )
    best_price = fields.Float (compute="_compute_best_price")
    total_area = fields.Float (compute="_compute_total_area")
    
    active=fields.Boolean(default=True)

    @api.depends("living_area","garden_area")
    def _compute_total_area(self):
        for rec in self:
            rec.total_area = rec.living_area + rec.garden_area

    @api.depends("offer_ids")
    def _compute_best_price(self):
        for rec in self:
            rec.best_price = max(rec.offer_ids.mapped("price"), default=0)

    @api.onchange("garden")
    def _onchange_garden(self):
        for estate in self:
            if not estate.garden:
                estate.garden_area = 0


    @api.onchange("date_availability")
    def _onchange_date_availability(self):
        for estate in self:
            if estate.date_availability and estate.date_availability < fields.Date.today():
                return {
                    "warning": {
                        "title": _("Warning"),
                        "message": _("The availability date has passed."),
                    }
                }
            


    def action_cancel(self):
        if self.state == 'sold':
            raise UserError(_('A sold property cannot be cancelled.'))
        self.state = 'cancelled'

    def action_sold(self):
        if self.state == 'cancelled':
            raise UserError(_('A cancelled property cannot be marked as sold.'))
        self.state = 'sold'

    @api.constrains("expected_price")
    def _check_constraint(self):
        for estate in self :
            if estate.expected_price <= 5000:
                raise ValidationError(_("The value should be greater than $5000"))
            
    
    