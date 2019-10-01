

# Extractor de recursos embebidos en ejecutables portables

Instrucciones:

Desarrollado en Python 2.7.

Define el nombre del recurso a extraer, recomiendo explorar primero el ejecutable con alguna herramienta tipo CFF Explorer. 

`resource_name = 'PSEXESVC'
`

Elige el tipo de extension con que extraerlo:


`expected_resource_type_to_export = '.exe'
`

Y el directorio donde está el o los ejecutables a explorar para la extracción:

`dir_path = 'pe_files_dir'
`

El script graba en un archivo XLSX los hash de cada recurso extraido y los propios recursos extraidos a la carpeta extracted.

`filename = 'extracted\\' + filename
`

Se incluye otro script `md5_files_dir.py` para generar los hashes de todos los archvos de una carpeta, así com su "import table hash" y añadirlos a un XLSX.
