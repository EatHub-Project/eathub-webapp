## Aviso
Esta carpeta contiene un dump de la base de datos con los datos de prueba por defecto de la aplicación. Contiene también dos scripts, en Batch y Shell Script, para exportar e importar el dump en la base de datos local.

### Importar base de datos
Utilizar el script `restore` para importar el dump de la carpeta *dump_data* a la base de datos MongoDB local.

```
AVISO:
Esto sobreescribe los datos almacenados.
```

### Exportar base de datos
Cuando se necesite exportar la base de datos, porque se añadan o actualicen los datos de prueba, se debe usar el script `dump`. Éste almacena en *dump_data* toda la información contenida en las colecciones *auth_user*, *webapp_profile* y *webapp_recipes*.

```
AVISO:
Los datos almacenados en la carpeta se sobrescriben. Es IMPORTANTE asegurarse de que los datos son correctos y están sólo los necesarios para el funcionamiento de la aplicación. Estos son los datos que usarán el resto de miembros del equipo, y que se mostrarán al público y al cliente.
```