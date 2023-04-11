from flask import Flask, render_template, request,redirect,url_for
from sqlalchemy import asc, desc, update
import db
from models import Tarea
from datetime import datetime, date

app=Flask(__name__,template_folder='templates')

@app.route("/")
def home():
    todas_las_tareas = db.session.query(Tarea).order_by(Tarea.fecha_limite).all() # Consultamos y almacenamos todas las tareas ordenadas por fecha ascendente
    #Ahora en la variable todas_las_tareas se tienen almacenadas todas las tareas en una lista de objetos. #Vamos a entregar esta variable al template index.html
    for tarea in todas_las_tareas:
        tarea.fecha_limite_editada = datetime.strptime(tarea.fecha_limite,"%Y-%m-%d")  # Se genera un bucle for iterando por cada atributo fecha limite y convirtiendo a class datetime para poder #con Jinja2 en HTML darle un formato adecuado.
        tarea.fecha_limite_editada = tarea.fecha_limite_editada.strftime("%d-%m-%Y")
    return render_template("index.html", lista_de_tareas=todas_las_tareas) #Se carga el template index.html

@app.route("/filtro-categoria", methods=["POST","GET"])
def filtro(): #Esta funcion filtra por tarea y ordena por fecha en orden ascendente
    filtro = request.form.get("filtro_categoria_tarea") #Comprobado que recibe el valor del form "filtro_categoria_tarea"
    query = db.session.query(Tarea).filter_by(categoria=str(filtro)).order_by(Tarea.fecha_limite).all()
    for tarea in query:
        tarea.fecha_limite_editada = datetime.strptime(tarea.fecha_limite,"%Y-%m-%d")  # Se genera un bucle for iterando por cada atributo fecha limite y convirtiendo a class datetime para poder #con Jinja2 en HTML darle un formato adecuado.
        tarea.fecha_limite_editada = tarea.fecha_limite_editada.strftime("%d-%m-%Y")
    db.session.close()
    return render_template("filtro-resultados.html", lista_de_filtros=query)

@app.route("/crear-tarea", methods=["POST"])
def crear(): #tarea es un objeto de la clase Tarea (una instancia de la clase) tarea = Tarea(contenido=request.form['contenido_tarea'], hecha=False) # id no es necesario asignarlo manualmente, porque la primary key se genera automaticamente db.session.add(tarea) # Añadir el objeto de Tarea a la base de datos db.session.commit() # Ejecutar la operación pendiente de la base de datos return "Tarea guardada" # Mensaje de log para ver a través del navegador
    tarea = Tarea(contenido=request.form["contenido_tarea"], categoria=request.form.get("categoria_tarea"), fecha_limite=request.form.get("fecha_limite_tarea"), hecha=False)
    db.session.add(tarea)  # Añadir el objeto de Tarea a la base de datos
    db.session.commit()  # Ejecutar la operación pendiente de la base de datos
    db.session.close()
    return redirect(url_for("home")) # Esto nos redirecciona a la función home()

@app.route("/eliminar-tarea/<id>")
def eliminar(id): #Elimina una tarea de la lista.
    tarea = db.session.query(Tarea).filter_by(id=int(id)).delete() # Se busca dentro de la base de datos,
    #aquel registro cuyo id coincida con el aportado por el parametro de la ruta. Cuando se encuentra se elimina
    db.session.commit() # Ejecutar la operación pendiente de la base de datos
    db.session.close()
    return redirect(url_for("home")) #Esto nos redirecciona a la función home() y si todo ha ido bien, al refrescar, la tarea eliminada ya no aparecera en el listado

@app.route("/tarea-hecha/<id>")
def hecha(id): #Realiza un tachado en la tarea que se resta hecha.
    tarea = db.session.query(Tarea).filter_by(id=int(id)).first() # Se obtiene la tarea que se busca
    tarea.hecha = not(tarea.hecha) # Guardamos en la variable booleana de la tarea, su contrario
    db.session.commit() # Ejecutar la operación pendiente de la base de datos
    db.session.close()
    return redirect(url_for("home")) # Esto nos redirecciona a la función home()

@app.route("/editar-tarea/<id>", methods=["POST","GET"])
def editar(id): #Se puede editar la tarea con esta función. Lo que no pude lograr es que pueda sobreescribir el contenido de la tarea al editarla.
    tarea = db.session.query(Tarea).filter_by(id=int(id)).first()
    tarea.fecha_limite_editada = datetime.strptime(tarea.fecha_limite,"%Y-%m-%d")  # Se genera un bucle for iterando por cada atributo fecha limite y convirtiendo a class datetime para poder #con Jinja2 en HTML darle un formato adecuado.
    tarea.fecha_limite_editada = tarea.fecha_limite_editada.strftime("%d-%m-%Y")
    print(tarea)
    return render_template("para-editar-tarea.html", tarea=tarea)

@app.route("/modificar-tarea/<id>", methods=["POST"])
def modificar_tarea(id): #Se guardan los cambios en la base de datos de la modificacion de la tarea.
    tarea = db.session.query(Tarea).filter_by(id=int(id)).first()
    contenido = request.form["contenido_tarea_edicion"]
    categoria = request.form["categoria_tarea_edicion"]
    fecha_limite = request.form["fecha_limite_tarea_edicion"]
    tarea = db.session.query(Tarea).filter(Tarea.id == id).update(
        {
            Tarea.contenido: contenido,
            Tarea.categoria: categoria,
            Tarea.fecha_limite: fecha_limite
        }
    )
    db.session.commit()
    db.session.close()
    tarea = db.session.query(Tarea).filter_by(id=int(id)).first()
    print("Tarea modificada con exito:\n{}".format(tarea)) #POR QUE TAREA SE CONVIERTE EN INT? Y COMO HAGO PARA VER POR CONSOLA LOS ATRIBUTOS DEL OBJETO ACTUALIZADO.
    return redirect(url_for("home"))  # Esto nos redirecciona a la función home()

######  FUNCIONES QUE INTENTE PERO NO PUDE REALIZAR CON EXITO  ######

@app.route("/eliminar-tarea-filtro/<id>")
def eliminar_filtro(id): #Elimina una tarea de la lista cuando se filtra por categoria sin volver a home.
    # Le cambie la ruta en en los botones de filtro-resultado cuando probé pero el error que me decia era que no se podia
    #construir la URL endpoint.
    tarea = db.session.query(Tarea).filter_by(id=int(id)).delete() # Se busca dentro de la base de datos,
    #aquel registro cuyo id coincida con el aportado por el parametro de la ruta. Cuando se encuentra se elimina
    tarea.fecha_limite_editada = datetime.strptime(tarea.fecha_limite,"%Y-%m-%d")  # Se genera un bucle for iterando por cada atributo fecha limite y convirtiendo a class datetime para poder #con Jinja2 en HTML darle un formato adecuado.
    tarea.fecha_limite_editada = tarea.fecha_limite_editada.strftime("%d-%m-%Y")
    db.session.commit() # Ejecutar la operación pendiente de la base de datos
    db.session.close()
    return redirect(url_for("filtro-resultados,html")) #Esto nos redirecciona a la función home() y si todo ha ido bien, al refrescar, la tarea eliminada ya no aparecera en el listado

@app.route('/tarea-hecha-filtro/<id>')
def hecha_filtro(id): #Marca como hecha la tarea cuando se filtra por categoria sin volver a home.
    # Le cambie la ruta en en los botones de filtro-resultado cuando probé, pero el error que me decia era que no se podia
    #construir la URL endpoint.
    tarea = db.session.query(Tarea).filter_by(id=int(id)).first() # Se obtiene la tarea que se busca
    tarea.hecha = not(tarea.hecha) # Guardamos en la variable booleana de la tarea, su contrario
    tarea.fecha_limite_editada = datetime.strptime(tarea.fecha_limite,"%Y-%m-%d")  # Se genera un bucle for iterando por cada atributo fecha limite y convirtiendo a class datetime para poder #con Jinja2 en HTML darle un formato adecuado.
    tarea.fecha_limite_editada = tarea.fecha_limite_editada.strftime("%d-%m-%Y")
    db.session.commit() # Ejecutar la operación pendiente de la base de datos
    db.session.close()
    return redirect(url_for("/filtro-resultados.html")) # Esto nos redirecciona a la función home()

@app.route("/fecha-actual/",methods=["POST","GET"])
def fecha_actual(): #esta función la hice para poder insertar el el html la fecha actual en la APP. Pero al querer usar Jinja2 no hubo manera.
    fecha_ahora = date.today()
    print(fecha_ahora)
    fecha_nueva = fecha_ahora.strftime("%d/%m/%Y")
    print(fecha_nueva)
    return fecha_nueva

if __name__ == "__main__":
    db.Base.metadata.create_all(db.engine)  # Creamos el modelo de datos
    app.run(debug=True)
