// Copyright (c) 2016, Raaj Tailor and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Ordered Items to be Delivered"] = {
	"filters": [
		{
			"fieldname":"status_type",
			"label": __("Status Type"),
			"fieldtype": "Select",
			"width": "80",
			// "options": ["Billed", "Not billed", "Not delivered", "Completed"],
			"options": ["To Deliver", "To Deliver and Bill","On Hold","To Bill"],
			"default": "To Deliver"
		},
		{
			"fieldname":"customer",
			"label": __("Customer"),
			"fieldtype": "Link",
			"options": "Customer"
		},
		{
			"fieldname":"warehouse",
			"label": __("Warehouse"),
			"fieldtype": "Link",
			"options": "Warehouse"
		},
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company"
		}
	]
};
