**Autor: Andrea Álvarez Pérez**														  									**3º Biotecnología, UPM**

# PROGRAMACIÓN PARA LA BIOINFORMÁTICA - PROYECTO FINAL

El proyecto final de la asignatura **Programación para la Bioinformática** se basa en un script que sea capaz de llevar a cabo varias tareas encadenadas. Cada tarea estará definida por un módulo al cual llamará el script principal.

- **Módulo 1:** *genbank_converter.py*

  Este módulo contiene una función: *convertidor_fasta*. Se encarga de parsear la carpeta que contiene todos los GenBank y fusionarlos en un único multifasta.

- **Módulo 2:** *query_analizer.py*

  Contiene dos funciones: *multifasta_fa* separa cada query del archivo multifasta aportado por el usuario en archivos fasta independientes para su posterior análisis.

  La función *comprobar_query* revisa cada query y comprueba que contiene el formato fasta correcto.

- **Módulo 3:** *blastp.py*

  Contiene dos funciones. La función *funcion_blast* realiza blastp sobre cada query separado utilizando como base de datos el archivo multifasta con los GenBanks.

  La función *filtro_blastp* va a filtrar estos resultados basándose en valores umbral de identity y coverage aportados por el usuario.

- **Módulo 4:** *muscle.py*

  La función *input_muscle* incluye en el archivo que se utilizará como input en el MUSCLE la secuencia del query original y la función *funcion_muscle* realiza el alineamiento múltiple y dibuja el árbol en formato .nw que se puede visualizar con iTOL.

- **Módulo 5:** *prosite.py*

  Contiene tres funciones. La primera, *prosite_db*, parsea el archivo prosite.dat que debe estar presente en la carpeta de ejecución y genera una base de datos. 

  La función *dictionary* genera un diccionario con la base de datos anterior transformandola en expresiones regulares y la función *domain_search* busca los dominios presentes en los hits del blastp y genera un archivo por query donde se muestra:

  - Nombre de la proteína
  - Nombre del dominio
  - Accession
  - Patrón encontrado
  - Descripción del dominio

Los resultados se almacenarán en una carpeta RESULTS, donde encontrará 3 subcarpetas:

- **Blastp_results**: hits del blastp **filtrados** nombrados como *"nombre del query_filtrado.fasta"*.
- **Muscle_results**: alineamientos y árboles llevados a cabo por MUSCLE nombrados como *"nombre del query_muscle.fa"* y *"nombre del query_muscle_tree.nw"*.
- **Prosite_results**: archivo *prosite_db* y archivos de texto con los dominios encontrados, nombrados como *"nombre del query_domains.txt"*.

## USO DEL SCRIPT

La forma correcta de ejecutar el script es:

```python
$ python main.py 'GENBANKS' 'QUERY' 'IDENTITY' 'COVERAGE'
```

Siendo:

- ``'GENBANKS'``:  nombre de la carpeta donde están almacenados los archivos .gbff sobre los que se desea crear la base de datos.
- ```'QUERY'```:  nombre de la carpeta donde está almacenado el archivo multifasta con los querys que se desean analizar.
- ``'IDENTITY'`` y ``'COVERAGE'``: valores numéricos que marcan el umbral de identity y coverage para filtrar los resultados del blastp. **Los hits que no pasen el filtro serán eliminados y no se analizarán en Prosite**.

A medida que se va ejecutando el script, en pantalla aparecerá un seguimiento de los pasos que se están realizando/se han realizado, avisando cuando se concluye e indicando las carpetas donde se pueden encontrar los archivos resultantes.

### Control de argumentos

El script principal controlará:

1. Que el número de argumentos introducido es correcto.
2. Que las carpetas para el ``'GENBANKS'`` y ```'QUERY'``` existen.
3. Que los valores de ``'IDENTITY'`` y ``'COVERAGE'`` son valores numéricos.

No cumplir cualquiera de estos 3 requisitos hará saltar la función *ayuda*, donde se le indicará el error cometido y como solventarlo.

## IMPORTANTE

Para la óptima ejecución del script se deben tener en cuenta:

- Las carpetas de los ``'GENBANKS'`` y ```'QUERY'``` deben encontrarse en la misma ubicación que el script principal *main.py*, así como del resto de módulos necesarios.
- El archivo *prosite.dat* debe encontrarse en la misma ubicación que el script principal y sus módulos.
- Las anotaciones de dentro del script están en **castellano**, pero durante la ejecución, lo impreso en pantalla se da en **inglés**.