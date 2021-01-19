odoo.define('pos_button.pos', function (require) {
"use strict";

var core = require('web.core');
var screens = require('point_of_sale.screens');
var models = require('point_of_sale.models');
var field_utils = require('web.field_utils');

var _t = core._t;


var existing_models = models.PosModel.prototype.models;
var product_index = _.findIndex(existing_models, function (model) {
    return model.model === "product.product";
});
var product_model = existing_models[product_index];


models.load_models([{
  model:  product_model.model,
  fields: product_model.fields,
  order:  product_model.order,
  domain: function(self) {return [['id', '=', self.config.disc_product_id[0]]];},
  context: product_model.context,
  loaded: product_model.loaded,
}]);

models.load_models({
    model: 'pos.order',
    fields: ['id', 'name', 'session_id', 'state', 'pos_reference', 'partner_id', 'amount_total','date_order'],
    domain: function(self){ [['id', '=', self.config.disc_product_id[0]]];},
    loaded: function (self, pos_orders)
    {
        self.pos_orders = pos_orders;
    }
});

var ShowDiscountButton = screens.ActionButtonWidget.extend({
    template: 'ShowDiscountButton',
    button_click: function(){

        var self = this;
        this.gui.show_popup('textinput',{
            'title': _t('Discount Percentage'),
            'value': this.pos.config.discount_pc,
            'confirm': function(val) {
                val = Math.round(Math.max(0,Math.min(100,field_utils.parse.float(val))));
                self.apply_discount(val);
            },
        });
    },
    apply_discount: function(pc) {
        var order    = this.pos.get_order();
        var lines    = order.get_orderlines();
        var product  = this.pos.db.get_product_by_id(this.pos.config.disc_product_id[0]);
        console.log(this.pos.config.disc_product_id[0])
        if (product === undefined) {
            this.gui.show_popup('error', {
                title : _t("No discount product found"),
                body  : _t("The discount product seems misconfigured. Make sure it is flagged as 'Can be Sold' and 'Available in Point of Sale'."),
            });
            return;
        }

        // Remove existing discounts
        var i = 0;
        while ( i < lines.length ) {
            if (lines[i].get_product() === product) {
                order.remove_orderline(lines[i]);
            } else {
                i++;
            }
        }

        // Add discount
        // We add the price as manually set to avoid recomputation when changing customer.
        var base_to_discount = order.get_total_without_tax();
        if (product.taxes_id.length){
            var first_tax = this.pos.taxes_by_id[product.taxes_id[0]];
            if (first_tax.price_include) {
                base_to_discount = order.get_total_with_tax();
            }
        }


        console.log(this.pos.config.pay)
        if(this.pos.config.pay == 'disc'){
                        var discount_price = - pc / 100.0 * base_to_discount;
            }

        else{
                        var discount_price = - pc;
            }
            console.log(order.get_subtotal())
            if(discount_price!=null){
                this.pos.discount_price = discount_price;
                this.pos.base_to_discount = base_to_discount;
            }
            else{
                this.pos.discount_price = 0;
                this.pos.base_to_discount = 0;
        }


        if( discount_price < 0 ){
        console.log("dis",this.discount_price)
            order.add_product(product,{
                price: discount_price,
                lst_price: discount_price,

                extras: {
                    price_manually_set: true,
                },
            });

        }
        console.log(this);

 },
})



var _super_order = models.Order.prototype;
models.Order = models.Order.extend({
   initialize: function() {
        _super_order.initialize.apply(this,arguments);
                   this.pos.discount_price = 0;

    },
    export_for_printing: function () {
        console.log("hello",this.pos.discount_price)
        var res = _super_order.export_for_printing.apply(this, arguments);
        res.discount_price = this.pos.discount_price;
        res.base_to_discount = this.pos.base_to_discount;

        return res;
    }
    })




screens.define_action_button({
    'name': 'discount',
    'widget': ShowDiscountButton,
    'condition': function(){

            return this.pos.config.pay && this.pos.config.disc_product_id;


    },
});


return {
    ShowDiscountButton: ShowDiscountButton

}

});