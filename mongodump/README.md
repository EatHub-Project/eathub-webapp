## Aviso
Esta carpeta contiene un dump en formato json de la base de datos con los datos de prueba por defecto de la aplicación. Contiene también dos scripts, en Batch y Shell Script, para exportar e importar el dump en la base de datos local.

### Importar base de datos
Utilizar el script `import` para importar el dump de la carpeta *exported_json* a la base de datos MongoDB local.

```
AVISO:
Esto elimina los datos almacenados previamente.
```

### Exportar base de datos
Cuando se necesite exportar la base de datos, porque se añadan o actualicen los datos de prueba, se debe usar el script `export`. Éste almacena en *exported_json* toda la información contenida en las colecciones *auth_user*, *webapp_profile*, *webapp_recipes* y *ajax_uploadedimage*.

```
AVISO:
Los datos almacenados en la carpeta se sobrescriben. Es IMPORTANTE asegurarse de que los datos son correctos y están sólo los necesarios para el funcionamiento de la aplicación. Estos son los datos que usarán el resto de miembros del equipo, y que se mostrarán al público y al cliente. No subir al repositorio datos innecesarios o incorrectos.
```

### Importar a Heroku / MongoHQ

1. Copiar la base de datos `eathub` al nombre que tenga la de MongoHQ, ej: `app22237589`
2. Hacer el dump de esa nueva base de datos con los mismo comandos de `dump.sh`
3. Hacer el restore especificando la dirección de la base de datos remota: `mongorestore -h troup.mongohq.com:10097 -d BD_NAME -u USER -p PASS ./mongodump/dump_data/DB_NAME/`
4. Be Happy :D