from flask import Blueprint, render_template, request, redirect, url_for, flash

from models import clients

app_client = Blueprint('app_client', __name__)

@app_client.route('/clientes', methods=['GET'])
def get_all():
    return render_template("allClients.html", Clients=clients.Clients)

@app_client.route('/clientes/editar/<int:client_id>', methods=['GET', 'POST'])
def edit_client(client_id):
    clientfound = [client for client in clients.Clients if client['id'] == client_id]

    if request.method == 'POST':
        if len(clientfound) > 0:
            clientfound[0]['name'] = request.form["Nombre"]
            clientfound[0]['Last_name'] = request.form["Apellidos"]
            clientfound[0]['address'] = request.form["Dirección"]
            clientfound[0]["postal_code"] = request.form["Código postal"]

            flash('Cliente actualizado', 'success')

            return redirect(url_for('app_client.get_all'))

    return render_template('edit_client.html')


@app_client.route('/clientes/eliminar/<int:client_id>', methods=['POST'])
def delete_client(client_id):
    clientfound = [client for client in clients.Clients if client['id'] == client_id]
    if len(clientfound) > 0:
        clients.Clients.remove(clientfound[0])

        flash('Cliente eliminado', 'success')

        return redirect(url_for('app_client.get_all'))

    if len(clientfound) == 0:
        return redirect(url_for('app_client.get_all'))


@app_client.route('/clientes/añadir', methods=['POST', 'GET'])
def add_client():
    if request.method == 'POST':
        new_client = {
            "id": int(request.form.get("id")),
            "name": request.form.get("Nombre"),
            "Last_name": request.form.get("Apellidos"),
            "address": request.form.get("Dirección"),
            "postal_code": request.form.get("Código postal")
        }
        clients.Clients.append(new_client)

        flash('Cliente añadido', 'success')

        return redirect(url_for('app_client.get_all'))

    return render_template('addClient.html')


@app_client.route('/clientes/<int:client_id>', methods=['GET'])
def search_id(client_id):
    clientfound = [client for client in clients.Clients if client['id'] == client_id]
    if len(clientfound) > 0:
        return render_template('oneClient.html', client=clientfound[0])

    if len(clientfound) == 0:
        return redirect(url_for('app_client.get_all'))
