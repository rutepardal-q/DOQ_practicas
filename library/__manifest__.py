# Copyright <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Library",
    "summary": "Module for managing a library",
    "version": "17.0.1.0.0",
    "category": "Sistema DOQ",
    "website": "https://www.qubiq.info",
    "author": "QubiQ",
    "license": "AGPL-3",
    "application": True,
    "installable": True,
    "depends": ['base', 'product', 'sale', 'mail'],
    "data": [
            "security/ir.model.access.csv",
            "security/library_security.xml",

            "wizard/deactivate_members_wizard.xml",
            "wizard/renting_wizard.xml",
            "wizard/returning_wizard.xml",
            "wizard/rental_history_wizard.xml",
            "wizard/warning_2rent_wizard.xml",




            "views/library_book.xml",
            "views/library_author.xml",
            "views/library_member.xml",
            "views/library_genre.xml",
            "views/library_audit.xml",
            "views/library_rental.xml",
            "views/library_rental_pivot.xml",
            "views/library_component.xml",
            "views/manual_reminder.xml",

            "views/res_partner.xml",
            "views/sale_order.xml",

            "views/report_book_template.xml",
            "views/report_book.xml",
            "views/report_sale.xml",
            "views/report_invoices.xml",

            "data/ir_cron.xml",
            "data/library_rent_mail_template.xml",


            "views/menus.xml",
            ],
}
