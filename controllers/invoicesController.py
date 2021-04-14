from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify

from models import invoices, clients, packages
from datetime import date

app_invoices = Blueprint('app_invoices', __name__)


def calculate_invoice(items):
    for item in items:
        total_invoice = item["price"] + item["track"]["cost"]

    return total_invoice


@app_invoices.route('/facturas')
def get_all():
    return render_template('allInvoices.html', Invoices=invoices.Invoices)


@app_invoices.route('/facturas/añadir', methods=['POST', 'GET'])
def add_invoice():
    if request.method == 'POST':
        new_invoice = {
            "id": int(request.form.get("id")),
            "total": 0.0,
            "date": date.fromisoformat(request.form.get("date")),
            "client": {
                "id": int(request.form.get("id client")),
                "name": request.form.get("name"),
                "Last_name": request.form.get("last_name"),
                "address": request.form.get("address"),
                "postal_code": int(request.form.get("postal_code"))
            },
            "items": []
        }
        invoices.Invoices.append(new_invoice)

        package_found = [package for package in packages.Packages if
                         package["id"] == int(request.form.get("id package"))]
        if len(package_found) > 0:
            new_invoice["items"].append(package_found[0])

        new_invoice["total"] = calculate_invoice(new_invoice["items"])

        flash('Factura añadida', 'success')

        return redirect(url_for('app_invoices.get_all'))
    return render_template('addInvoice.html')


@app_invoices.route('/facturas/editar/<int:invoice_id>', methods=['POST', 'GET'])
def edit_invoice(invoice_id):
    invoice_found = [invoice for invoice in invoices.Invoices if invoice["id"] == invoice_id]
    if request.method == 'POST':
        if len(invoice_found) > 0:
            invoice_found[0]["id"] = request.form.get("id")
            invoice_found[0]["total"] = request.form.get("total")

            flash('Factura actualizada', 'success')

            return redirect(url_for('app_invoices.get_all'))
    return render_template('editInvoice.html')


@app_invoices.route('/facturas/eliminar/<int:invoice_id>', methods=['POST'])
def delete_invoice(invoice_id):
    invoice_found = [invoice for invoice in invoices.Invoices if invoice["id"] == invoice_id]
    if len(invoice_found) > 0:
        invoices.Invoices.remove(invoice_found[0])

        flash('Factura eliminada', 'success')

        return redirect(url_for('app_invoices.get_all'))

    if len(invoice_found) == 0:
        return redirect(url_for('app_invoices.get_all'))


@app_invoices.route('/facturas/<int:invoice_id>', methods=['GET'])
def search_id(invoice_id):
    invoice_found = [invoice for invoice in invoices.Invoices if invoice["id"] == invoice_id]
    if len(invoice_found) > 0:
        return render_template('oneInvoice.html', invoice=invoice_found[0])
    if len(invoice_found) == 0:
        return redirect(url_for('app_invoices.get_all'))


@app_invoices.route('/facturas/añadir_paquete/<int:invoice_id>', methods=['GET', 'POST'])
def add_package(invoice_id):
    if request.method == 'POST':
        invoice_found = [invoice for invoice in invoices.Invoices if invoice["id"] == invoice_id]
        if len(invoice_found) > 0:
            package_found = [package for package in packages.Packages if package["id"] == int(request.form.get("id package"))]
            if len(package_found) > 0:
                invoice_found[0]["items"].append(package_found[0])
                invoice_found[0]["total"] = invoice_found[0]["total"] + calculate_invoice(invoice_found[0]["items"])
                return redirect(url_for('app_invoices.get_all'))
        else:
            return redirect(url_for('app_invoices.get_all'))
    return render_template('addInvoicePackage.html')


@app_invoices.route('/facturas/eliminar_paquete/<int:invoice_id>', methods=['GET', 'POST'])
def delete_package(invoice_id):
    if request.method == 'POST':
        invoice_found = [invoice for invoice in invoices.Invoices if invoice["id"] == invoice_id]
        if len(invoice_found) > 0:
            package_found = [package for package in invoice_found[0]["items"] if package["id"] == int(request.form.get("id package"))]
            if len(package_found) > 0:
                invoice_found[0]["total"] = invoice_found[0]["total"] - calculate_invoice(invoice_found[0]["items"])
                invoice_found[0]["items"].remove(package_found[0])
                return redirect(url_for('app_invoices.get_all'))
            else:
                return redirect(url_for('app_invoices.delete_package', invoice_id=invoice_id))
        else:
            return redirect(url_for('app_invoices.get_all'))
    return render_template('deleteInvoicePackage.html')

