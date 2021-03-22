odoo.define('pos_button.pos', function (require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const { useListener } = require('web.custom_hooks');
    const Registries = require('point_of_sale.Registries');


    class ShowDiscountButton extends PosComponent {
        constructor() {
            super(...arguments);
            useListener('click', this.onClick);
        }
        async onClick() {
            var self = this;
            const { confirmed, payload } = await this.showPopup('TextInputPopup',{
                title: this.env._t('Discount'),
            });
            if (confirmed) {
                const val = Math.round(Math.max(0,Math.min(100,parseFloat(payload))));
                await self.apply_discount(val);
            }
        }

        async apply_discount(pc) {
            var order    = this.env.pos.get_order();
            var lines    = order.get_orderlines();
            var product  = this.env.pos.db.get_product_by_id(this.env.pos.config.disc_product_id[0]);
            if (product === undefined) {
                await this.showPopup('ErrorPopup', {
                    title : this.env._t("No discount product found"),
                    body  : this.env._t("The discount product seems misconfigured. Make sure it is flagged as 'Can be Sold' and 'Available in Point of Sale'."),
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
                var first_tax = this.env.pos.taxes_by_id[product.taxes_id[0]];
                if (first_tax.price_include) {
                    base_to_discount = order.get_total_with_tax();
                }
            }
            console.log(this.env.pos.config.pay)
            console.log(this.env.pos.config.disc_product_id[0])
            if (this.env.pos.config.pay == 'disc'){
                        var discount_price = - pc / 100.0 * base_to_discount;

            }
            else{
                        var discount_price = - pc;

            }
            if(discount_price!=null){
                this.env.pos.discount_price = discount_price;
                this.env.pos.base_to_discount = base_to_discount;
                this.env.pos.disc = pc;
                }
                            console.log("->",this.env.pos.discount_price)


            if( discount_price < 0 ){
                order.add_product(product, {
                    price: discount_price,
                    lst_price: discount_price,
                    extras: {
                        price_manually_set: true,
                    },
                });
            }
        }
            }


    var models = require('point_of_sale.models');
    var _super_order = models.Order.prototype;

    models.Order = models.Order.extend({
       initialize: function() {
        _super_order.initialize.apply(this,arguments);
                   this.pos.discount_price = 0;
                   this.pos.base_to_discount = 0;

    },

        export_for_printing: function () {
            var result = _super_order.export_for_printing.apply(this, arguments);
            result.discount_price = this.pos.discount_price;
            result.base_to_discount = this.pos.base_to_discount;
            result.mode = this.pos.config.pay;
            result.discount_pc = this.pos.disc;
            return result;
        }
        })

    ShowDiscountButton.template = 'ShowDiscountButton';

    ProductScreen.addControlButton({
        component: ShowDiscountButton,
        condition: function() {
            return this.env.pos.config.pay && this.env.pos.config.disc_product_id && this.env.pos.config.en_discount;
        },
    });

    Registries.Component.add(ShowDiscountButton);



    return ShowDiscountButton;
});

