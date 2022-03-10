Scrapers a distintas páginas de alquileres de casas, phs y deptos en CABA, Argentina.
Los datos levantados se utilizarán en el marco de un proyecto universitario interdisciplinario que busca estudiar el acceso a los espacios verdes y la calidad de los mismos dentro de CABA.

Por ahora las páginas scrapeadas son MercadoLibre y Properati.
Los scrapers pueden ser ejecutados individualmente, pasandole como argumento un directorio donde guardará los archivos csvs de la forma "YYYY-MM-DD_PaginaWeb_TipoDeVivienda.csv".
O bien pueden ser ejecutados secuencialmente con el script de bash "scrap_inmobs.sh " pasandole el mismo argumento. "scrap_inmobs.sh además creará un log_file donde escribe cuando se ejecutan los scrapers individuales, y registrará también en él si ocurre un error con los mismos."
