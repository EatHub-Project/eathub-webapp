#!/bin/bash
clear
echo "Este script es un asistente para actualizar las traducciones de la web."
echo "                  ========="
echo "Primero se ejecutará un makemessages para actualizar la lista de cadenas de los archivos de traducción .po."
echo ""
echo "Después se hará una pausa para que puedas rellenar las traducciones vacías"
echo "(puedes comprobar qué se ha modificado con el diff del repositorio)."
echo ""
echo "Cuando termines de traducir, continúa el script para compilar los archivos de traducción .mo."
echo ""
echo "-----"
read -p "Pulsa una tecla para comenzar a procesar los archivos de traducción…"
echo ""

cd ..
django-admin.py makemessages -a --ignore venv
echo "----"
echo ""
echo "Archivos .po actualizados. Ahora añade las traducciones necesarias. Ayúdate del control de versiones si es necesario."
echo "Asegúrate de que todo está como debe antes de continar, después de compilar no se deben modificar los archivos de traducción."
echo ""
read -p "Pulsa una tecla cuando termines para comenzar a compilar las traducciones..."
echo ""
django-admin.py compilemessages
echo "----"
echo ""
echo "LISTO! Ya puedes subir los cambios al repositorio."