

# Extractor de Recursos embebidos en ejecutables portables

Instrucciones:

Define el nombre del recurso a extraer, recomiendo explorar primero el ejecutable con alguna herramienta tipo CFF Explorer. 

`resource_name = 'PSEXESVC'
`

Elige el tipo de extension con que extraerlo:

`expected_resource_type_to_export = '.exe'
`


Y el directorio donde está el o los ejecutables a explorar para la extracción:
`dir_path = 'pe_files_dir'
`

El script graba en un archivo XLSX los hash de cada recurso extraido.
