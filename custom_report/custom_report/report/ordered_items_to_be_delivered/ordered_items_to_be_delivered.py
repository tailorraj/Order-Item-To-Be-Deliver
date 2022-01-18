# Copyright (c) 2013, Raaj Tailor and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	columns, data = get_columns(filters), get_data(filters)
	return columns, data


def get_data(filters):
	# value = {'status_type': filters.status_type}
	conditions=get_conditions(filters)
	# frappe.msgprint(str(conditions))
	get_data = frappe.db.sql("""
			select 
		`tabSales Order`.`transaction_date` as date,
		`tabSales Order`.`status` as status,
		`tabSales Order`.`name` as sales_order,
		`tabSales Order`.`customer_name` as customer,
		`tabSales Order Item`.item_code as item,
		`tabItem`.item_group as item_grp,
		`tabSales Order Item`.qty as quantity,
		`tabSales Order Item`.rate as rate,
		`tabSales Order Item`.warehouse as warehouses,
		`tabBin`.actual_qty as available_qty,
		`tabBin`.projected_qty as projected_q,  
		`tabSales Order Item`.delivered_qty as delivered_q,
		`tabSales Order Item`.qty - `tabSales Order Item`.delivered_qty as bal_q,
		`tabSales Order`.`company` as companies
		from
		`tabSales Order` JOIN `tabSales Order Item` 
		LEFT JOIN `tabBin` ON (`tabBin`.item_code = `tabSales Order Item`.item_code
		and `tabBin`.warehouse = `tabSales Order Item`.warehouse)
		LEFT JOIN `tabItem` ON `tabSales Order Item`.item_code = `tabItem`.name
		where
		`tabSales Order Item`.`parent` = `tabSales Order`.`name`
		and `tabSales Order`.docstatus = 1
		and `tabSales Order`.status not in ("Stopped", "Closed")
		and ifnull(`tabSales Order Item`.delivered_qty,0) < ifnull(`tabSales Order Item`.qty,0) {conditions}
		order by `tabSales Order`.transaction_date asc
	""".format(conditions=get_conditions(filters)),filters,as_dict=1)
	
	return get_data

def get_conditions(filters):
	conditions = []
	if filters.get("status_type"):
		conditions.append("`tabSales Order`.status=%(status_type)s")
	
	if filters.get("customer"):
		conditions.append("`tabSales Order`.customer=%(customer)s")

	if filters.get("warehouse"):
		conditions.append("`tabSales Order Item`.warehouse=%(warehouse)s")
	
	if filters.get("company"):
		conditions.append("`tabSales Order`.company=%(company)s")
	return "and {}".format(" and ".join(conditions)) if conditions else ""

def get_columns(filters):
	columns = [
		{
			"label":_("Date"),
			"fieldname": "date",
			"fieldtype": "Date",
			"width": 100
		},
		{
			"label":_("Status"),
			"fieldname": "status",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label":_("Sales Order"),
			"fieldname": "sales_order",
			"fieldtype": "Link",
			"options": "Sales Order",
			"width": 120
		},
		{
			"label":_("Customer Name"),
			"fieldname": "customer",
			"fieldtype": "Link",
			"options": "Customer",
			"width": 150
		},
		{
			"label":_("Items"),
			"fieldname": "item",
			"fieldtype": "Data",
			"width": 150
		},
		{
			"label":_("Item Group"),
			"fieldname": "item_grp",
			"fieldtype": "Data",
			"width": 150
		},
		{
			"label":_("Qty"),
			"fieldname": "quantity",
			"fieldtype": "float",
			"width": 50
		},
		{
			"label":_("Unit Price"),
			"fieldname": "rate",
			"fieldtype": "Currency",
			"width": 100
		},
		{
			"label":_("Warehouse"),
			"fieldname": "warehouses",
			"fieldtype": "Link",
			"options": "Warehouse",
			"width": 150
		},
		{
			"label":_("Available Qty"),
			"fieldname": "available_qty",
			"fieldtype": "float",
			"width": 100
		},
		{
			"label":_("Projected Qty"),
			"fieldname": "projected_q",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label":_("Delivered Qty"),
			"fieldname": "delivered_q",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label":_("Bal Qty"),
			"fieldname": "bal_q",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label":_("Company"),
			"fieldname": "companies",
			"fieldtype": "Link",
			"options": "Company",
			"width": 150
		},
	]
	return columns



