odoo.define('pos_owner.PosProductOwner', function (require) {
"use strict";
console.log("Entered")

var models = require('point_of_sale.models');

models.load_fields('product.product', ['owner_name']);
console.log("loaded")

var _super_orderline = models.Orderline.prototype;
models.Orderline = models.Orderline.extend({
    export_for_printing: function() {
        var line = _super_orderline.export_for_printing.apply(this,arguments)
        line.owner_name = this.get_product().owner_name;
        return line;


    },
    });

});