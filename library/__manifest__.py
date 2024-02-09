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
    "depends": ['base', 'product', 'sale'],
    "data": ["security/ir.model.access.csv",
             "security/library_security.xml",
             "views/library_author.xml",
             "views/library_member.xml",
             "views/library_genre.xml",
             "views/library_audit.xml",
             "views/library_book.xml",
             "views/res_partner.xml",
             "views/library_component.xml",
             "views/menus.xml"
             ],
}
