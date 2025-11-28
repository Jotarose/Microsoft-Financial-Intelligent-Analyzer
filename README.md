# Microsoft Investor Scrapper

Proyecto en Python para extraer y estructurar los datos financieros publicados en los informes anuales de Microsoft (Investor Relations).

Este repositorio contiene un pequeño scrapper orientado a obtener las tablas de estados financieros (p. ej. "INCOME STATEMENTS"), normalizarlas y guardarlas en JSON para su posterior análisis.

## Contenido rápido

- **Proyecto**: `web-scrapper` — extrae y guarda datos financieros de los informes anuales de Microsoft.
- **Lenguaje**: Python 3.10+
- **Salida**: `downloads/all_ms_financial_data.json` (JSON estructurado por año).

## Tabla de contenidos

1. [Instalación](#instalaci%C3%B3n)
2. [Uso](#uso)
3. [Estructura del proyecto](#estructura-del-proyecto)
4. [Formato de salida](#formato-de-salida)
5. [Consideraciones importantes](#consideraciones-importantes)
6. [Contribuir](#contribuir)
7. [Contacto y licencia](#contacto-y-licencia)

## Instalación

Recomendado: crear un entorno virtual y usar `pip`.

En PowerShell (Windows):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -U pip
pip install -e .
```

Notas:

- Si no usas `pip install -e .`, puedes instalar directamente las dependencias listadas en `pyproject.toml` con `pip install requests beautifulsoup4 lxml`.
- El proyecto reclama Python >= 3.10 (ver `pyproject.toml`).

## Uso

El punto de entrada es el script `main.py` en la raíz del proyecto. Ejecuta el script desde la raíz del repositorio:

```powershell
.\.venv\Scripts\Activate.ps1
python main.py
```

Al ejecutarlo, el flujo general es:

1. `src.client.MicrosoftIRClient` recopila las URLs de los informes anuales.
2. `main.py` usa un `ThreadPoolExecutor` para paralelizar la extracción por año.
3. `src.worker.extract_financial_data` descarga la página del informe, localiza la tabla "INCOME STATEMENTS" y la transforma a un diccionario estructurado.
4. `src.utils.parse_data` y `src.utils.save_data` limpian y serializan la salida final en `downloads/all_ms_financial_data.json`.

## Estructura del proyecto

- `main.py`: Orquestador principal. Inicializa el cliente, lanza workers en paralelo y guarda el resultado final en `downloads/all_ms_financial_data.json`.
- `pyproject.toml`: Metadatos del proyecto y dependencias (definidas para `requests`, `beautifulsoup4`, `lxml`, etc.).
- `README.md`: Este archivo.
- `downloads/`:
  - `all_ms_financial_data.json`: Resultado de la ejecución — JSON con los datos extraídos por año.
- `src/`:
  - `__init__.py`: Inicializador del paquete.
  - `client.py`: Contiene la clase `MicrosoftIRClient` y el `dataclass` `Report`.
    - `MicrosoftIRClient.get_annual_reports()`: Obtiene enlaces a informes anuales (busca etiquetas `<a>` con `aria-label` que coincidan).
    - `MicrosoftIRClient.get_url_content(url)`: Descarga el HTML de una URL dada.
  - `utils.py`: Helpers para manejar rutas y serialización.
    - `handle_file_path(file_name)`: Asegura que la carpeta `downloads/` exista y devuelve la ruta completa.
    - `parse_data(all_reports)`: Convierte la lista de dicts retornada por los workers a un diccionario por año.
    - `save_data(file_path, report)`: Guarda el JSON de salida (maneja errores básicos I/O).
  - `worker.py`: Lógica de extracción HTML y parsing de la tabla contigua a la cadena "INCOME STATEMENTS".
    - `extract_financial_data(client, report)`: Devuelve un diccionario con la forma `{ "year": <año>, "data": { <secciones>: {<items>: <valor>} } }` o `{ "year": <año>, "error": "Tabla no encontrada" }`.
- `web_scrapper.egg-info/`: Metadatos generados por herramientas de empaquetado (ignorarlo para el desarrollo diario).

## Formato de salida

La salida en `downloads/all_ms_financial_data.json` es un objeto JSON donde cada clave es un año (como cadena) y su valor es:

- Un objeto con secciones (por ejemplo, `"Revenue:"`, `"Cost of revenue:"`) y dentro de cada sección un diccionario con items y valores.
- Si la tabla no se encuentra para un año, el valor puede ser la cadena `"Tabla no encontrada"` o un objeto que contenga `"error"`.

Ejemplo resumido (ya presente en `downloads/all_ms_financial_data.json`):

```json
{
  "2024": {
    "Revenue:": {
      "Product": "$64,773",
      "Service and other": "180,349",
      "Total revenue": "245,122"
    },
    "Net income": { "Total": "$88,136" }
  }
}
```

## Consideraciones importantes

- Legal y ética: Antes de hacer scraping a un sitio público, revisa `robots.txt` y los términos de uso del sitio. Este proyecto está pensado para aprender y procesar informes públicos; respeta las políticas de Microsoft y evita generar carga innecesaria.
- Robustez: El HTML de los informes puede variar entre años. El extractor busca texto literal `INCOME STATEMENTS` y usa clases CSS como `cell-indent` y `cell-indent-double` para deducir jerarquía; esto puede romperse si el sitio cambia.
- Retries y límites: Añadir reintentos exponenciales y límites de velocidad (sleep/backoff) es recomendable para producción.
- Internacionalización: Fechas y formatos numéricos pueden necesitar limpieza adicional (por ejemplo, quitar comas, paréntesis, signos de moneda) antes de análisis numérico.

## Depuración y pruebas rápidas

- Para depurar un año concreto puedes editar `main.py` para iterar solo sobre el `report` deseado o usar el REPL e invocar `MicrosoftIRClient` y `extract_financial_data` manualmente.
- Para ver el contenido ya extraído, abre `downloads/all_ms_financial_data.json` con tu editor o un visualizador de JSON.

## Cómo contribuir

Proceso para contribuir:

1. Fork del repositorio.
2. Crear una rama de feature: `git checkout -b feat/nombre-feature`.
3. Hacer PR con descripción clara y tests incluidos.

## Contacto y licencia

Si necesitas contactar al autor original, `juan.arabaolaza@gmail.com` (ver `pyproject.toml`).
