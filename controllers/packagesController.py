from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify

from models import packages, tracks

app_packages = Blueprint('app_packages', __name__)


def track_service(destination_name):
    trackFound = [track for track in tracks.Tracks if track["destination"] == destination_name]

    if len(trackFound) > 0:
        return trackFound[0]["cost"]
    else:
        return 'trayectoria no encontrada'


@app_packages.route('/paquetes')
def get_all():
    return render_template('allPackages.html', Packages=packages.Packages)


@app_packages.route('/paquetes/añadir', methods=['POST', 'GET'])
def add_package():
    if request.method == 'POST':
        new_package = {
            "id": int(request.form.get("id")),
            "name": request.form.get("Name"),
            "price": float(request.form.get("Price")),
            "track": {
                "id": request.form.get("id track"),
                "origin": request.form.get("origen"),
                "destination": request.form.get("destino"),
                "cost": track_service(request.form.get("destino"))
            }
        }
        packages.Packages.append(new_package)

        flash('Paquete añadido', 'success')

        return redirect(url_for('app_packages.get_all'))
    return render_template('addPackage.html')


@app_packages.route('/paquetes/editar/<int:package_id>', methods=['POST', 'GET'])
def edit_package(package_id):
    package_found = [package for package in packages.Packages if package["id"] == package_id]
    if request.method == 'POST':
        if len(package_found) > 0:
            package_found[0]["name"] = request.form.get("Name")
            package_found[0]["price"] = request.form.get("Price")
            package_found[0]["track"]["origin"] = request.form.get("origen")
            package_found[0]["track"]["destination"] = request.form.get("destino")
            package_found[0]["track"]["cost"] = track_service(request.form.get("destino"))

            flash('Paquete actualizado', 'success')

            return redirect(url_for('app_packages.get_all'))
    return render_template('editPackage.html')


@app_packages.route('/paquetes/eliminar/<int:package_id>', methods=['POST'])
def delete_package(package_id):
    package_found = [package for package in packages.Packages if package["id"] == package_id]
    if len(package_found) > 0:
        packages.Packages.remove(package_found[0])

        flash('Paquete eliminado', 'success')

        return redirect(url_for('app_packages.get_all'))

    if len(package_found) == 0:
        return redirect(url_for('app_packages.get_all'))


@app_packages.route('/paquetes/<int:package_id>', methods=['GET'])
def search_id(package_id):
    package_found = [package for package in packages.Packages if package["id"] == package_id]
    if len(package_found) > 0:
        return render_template('onePackage.html', package=package_found[0])
    if len(package_found) == 0:
        return redirect(url_for('app_packages.get_all'))

