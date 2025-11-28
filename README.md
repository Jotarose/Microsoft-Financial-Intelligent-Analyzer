# Microsoft Investor Scrapper

Proyecto en Python para extraer y estructurar los datos financieros publicados en los informes anuales de Microsoft (Investor Relations).

Este repositorio contiene un pequeño scrapper orientado a obtener las tablas de estados financieros (p. ej. "INCOME STATEMENTS"), normalizarlas y guardarlas en JSON para su posterior análisis.

## Contenido rápido

- **Proyecto**: `web-scrapper` — extrae y guarda datos financieros de los informes anuales de Microsoft.
- **Lenguaje**: Python 3.10+
- **Salida**: `downloads/all_ms_financial_data.json` (JSON estructurado por año).

## Tabla de contenidos

1. [Instalación](#instalacion)
2. [Uso](#uso)
3. [Estructura del proyecto](#estructura-del-proyecto)
4. [Funcionalidades principales](#funcionalidades-principales)
5. [IA con Gemini](#ia-con-gemini)
6. [Gráficas y visualizaciones](#gráficas-y-visualizaciones)
7. [Formato de salida](#formato-de-salida)
8. [Consideraciones importantes](#consideraciones-importantes)
9. [Contribuir](#contribuir)
10. [Contacto y licencia](#contacto-y-licencia)

## Instalación

Recomendado: crear un entorno virtual y usar `pip`.

En PowerShell (Windows):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -U pip
pip install -e .
```

Notas:

- Si no usas `pip install -e .`, puedes instalar directamente las dependencias listadas en `pyproject.toml`.
- El proyecto reclama Python >= 3.10 (ver `pyproject.toml`).
- **Variables de entorno requeridas**: Para usar la funcionalidad de IA con Gemini, debes crear un archivo `.env` en la raíz del proyecto con tu clave API:
  ```
  GEMINI_API_KEY=tu_clave_api_aqui
  ```
  Obtén tu clave en [Google AI Studio](https://aistudio.google.com/app/apikey).

## Uso

El punto de entrada es el script `main.py` en la raíz del proyecto. Ejecuta el script desde la raíz del repositorio:

```powershell
.\.venv\Scripts\Activate.ps1
python main.py
```

Al ejecutarlo, el flujo general es:

1. **Extracción web**: `src.client.MicrosoftIRClient` recopila las URLs de los informes anuales de Microsoft IR.
2. **Paralización de workers**: `main.py` usa un `ThreadPoolExecutor` para paralelizar la extracción por año.
3. **Parsing de tablas**: `src.worker.extract_financial_data` descarga la página del informe, localiza la tabla "INCOME STATEMENTS" y la transforma a un diccionario estructurado.
4. **Limpieza y serialización**: `src.utils.parse_data` y `src.utils.save_data` guardan el JSON en `downloads/all_ms_financial_data.json`.
5. **Análisis con IA**: `src.gemini_ai.generate_financial_tesis` genera un análisis profesional usando **Gemini AI** (requiere `GEMINI_API_KEY` en `.env`).
6. **Visualización**: `src.visualization.generate_tables` genera gráficas comparativas de ingresos y rentabilidad usando **matplotlib** y **seaborn**.

## Estructura del proyecto

- `main.py`: Orquestador principal. Gestiona extracción, IA, visualización y guardado de resultados.
- `pyproject.toml`: Metadatos, dependencias (incluyendo `google-genai`, `matplotlib`, `pandas`, `seaborn`).
- `README.md`: Este archivo.
- `downloads/`:
  - `all_ms_financial_data.json`: Datos financieros extraídos por año.
  - `financial_tesis.md`: Análisis generado por Gemini AI.
- `tests/`:
  - `test_client.py`: Tests unitarios para `MicrosoftIRClient`.
  - `test_worker.py`: Tests para extracción de datos financieros.
  - `test_utils.py`: Tests para funciones de utilidad.
- `src/`:
  - `__init__.py`: Inicializador del paquete.
  - `client.py`: Cliente HTTP para descargar informes de Microsoft IR.
    - `MicrosoftIRClient.get_annual_reports()`: Obtiene enlaces a informes anuales.
    - `MicrosoftIRClient.get_url_content(url)`: Descarga HTML de una URL.
  - `worker.py`: Extracción y parsing de tablas financieras.
    - `extract_financial_data(client, report)`: Parsea "INCOME STATEMENTS" y devuelve diccionario estructurado.
  - `utils.py`: Helpers para rutas, serialización y guardado.
    - `handle_file_path(file_name)`: Crea carpeta `downloads/` si no existe.
    - `parse_data(all_reports)`: Convierte lista de reports a diccionario por año.
    - `save_data(file_path, report)`: Guarda JSON con manejo de errores.
    - `save_tesis(file_path, tesis)`: Guarda texto generado por IA.
  - **`gemini_ai.py`** (NUEVO): Análisis con IA usando Gemini 2.5 Pro.
    - `generate_financial_tesis(financial_data)`: Genera tesis de inversión con análisis profesional.
    - Requiere `GEMINI_API_KEY` en `.env`.
  - **`visualization.py`** (NUEVO): Gráficas y visualizaciones.
    - `generate_tables(raw_financial_data)`: Crea gráficas de ingresos y rentabilidad.
    - Limpia valores financieros (símbolos de moneda, paréntesis, comas).
    - Usa matplotlib + seaborn para visualización profesional.
- `web_scrapper.egg-info/`: Metadatos generados por pip (ignorar).

## Funcionalidades principales

### 1. Extracción de datos financieros

- Descarga automática de informes anuales desde el portal de Investor Relations de Microsoft.
- Parseo HTML inteligente con `BeautifulSoup` para extraer tablas "INCOME STATEMENTS".
- Procesamiento paralelo con `ThreadPoolExecutor` para máximo 6 años simultáneamente.
- Manejo robusto de errores y datos faltantes.

### 2. Análisis con IA (Gemini)

- Genera **tesis de inversión profesionales** usando el modelo Gemini 2.5 Pro de Google.
- Análisis automatizado que incluye:
  - Transformación del modelo de negocio (Product vs. Service revenue).
  - Márgenes de beneficio e "Operating Leverage".
  - Eficiencia de R&D y crecimiento esperado.
  - Recomendación de compra/mantenimiento/venta.

### 3. Visualización de datos

- Gráficas interactivas usando `matplotlib` y `seaborn`.
- Comparativa de ingresos por línea de negocio (stacked bar chart).
- Análisis de crecimiento vs. rentabilidad (dual line chart).
- Formateo profesional de ejes con separadores de miles.

## IA con Gemini

### Funcionalidad

`src/gemini_ai.py` implementa análisis inteligente de estados financieros:

```python
from src.gemini_ai import generate_financial_tesis

# Genera un análisis profesional en formato Markdown
tesis = generate_financial_tesis(financial_data)
print(tesis)
```

### Requisitos

1. Crear un archivo `.env` en la raíz del proyecto:
   ```
   GEMINI_API_KEY=tu_api_key_aqui
   ```
2. Obtener clave API gratuita en [Google AI Studio](https://aistudio.google.com/app/apikey).

### Salida

El análisis incluye:

- **Memo ejecutivo** con resumen del desempeño.
- **Análisis de márgenes**: Gross Margin, Operating Margin, Net Profit Margin.
- **Crecimiento**: CAGR de ingresos y EPS.
- **Recomendación**: Buy/Hold/Sell con justificación fundamentada.
- **Riesgos identificados**: Basados en tendencias de los últimos 11 años.

Ejemplo de salida guardada en `downloads/financial_tesis.md`.

## Gráficas y visualizaciones

### Funcionalidad

`src/visualization.py` genera visualizaciones automáticas:

```python
from src.visualization import generate_tables

# Genera dos gráficas profesionales
generate_tables(financial_data)
```

### Gráficas generadas

#### 1. Business Model Transformation (Gráfico de barras apiladas)

Muestra la evolución del mix de ingresos:

- **Eje X**: Años (2015–2025)
- **Eje Y**: Ingresos en millones USD
- **Categorías**:
  - Azul oscuro: Ingresos de Productos
  - Verde: Ingresos de Servicios y otros

**Insight**: Demuestra cómo Microsoft pasó de un modelo orientado a productos (2015) a uno dominado por servicios cloud (2025).

#### 2. Growth vs. Profitability (Gráfico de líneas dual)

Compara crecimiento absoluto con rentabilidad:

- **Línea azul** (con círculos): Total de Ingresos
- **Línea naranja** (con cuadrados y discontinua): Beneficio Neto

**Insight**: Muestra si la empresa crece manteniéndose rentable o si el crecimiento sacrifica márgenes.

### Limpieza de datos

La función `parse_financial_value()` normaliza valores financieros:

- Elimina símbolos `$` y comas (ej: `"$1,234"` → `1234.0`).
- Convierte números negativos en paréntesis `(100)` → `-100.0`.
- Devuelve `0.0` para valores vacíos o no parseables.

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

### 2. Análisis IA (`financial_tesis.md`)

Documento Markdown con análisis profesional generado por Gemini:

```markdown
### [INTERNAL MEMO]

**Objetivo:** Análisis de inversión de Microsoft (2014–2025)

**Tesis Principal:**
Microsoft ha realizado una transformación del modelo de negocio...
[Análisis detallado de márgenes, crecimiento, riesgos, y recomendación]
```

Se guarda en `downloads/financial_tesis.md` al ejecutar `main.py`.

### 3. Gráficas interactivas

Al ejecutar `main.py`, se muestran dos gráficos matplotlib:

- **Gráfico 1**: Stacked bar chart (Product vs Service revenue).
- **Gráfico 2**: Dual line chart (Total Revenue vs Net Income).

## Consideraciones importantes

### Extracción web

- **Legal y ética**: Antes de hacer scraping a un sitio público, revisa `robots.txt` y los términos de uso. Este proyecto está pensado para aprender; respeta las políticas de Microsoft.
- **Robustez HTML**: El HTML de los informes puede variar entre años. El extractor busca texto literal "INCOME STATEMENTS" y clases CSS como `cell-indent`.
- **Retries**: Para producción, añade reintentos exponenciales y límites de velocidad (`sleep`/backoff).

### IA con Gemini

- **API Key**: Requiere `GEMINI_API_KEY` en `.env`. Las solicitudes sin clave o con cuota agotada fallarán gracefully.
- **Idioma**: El análisis se genera en español (configurable en `src/gemini_ai.py`).
- **Costos**: Google ofrece cuota gratuita para desarrollo. Consulta [pricing](https://ai.google.dev/pricing) para uso en producción.

### Visualizaciones

- **Dependencias gráficas**: Usa `matplotlib` + `seaborn`. En entornos sin display (servidores), asegúrate de usar backend no interactivo (`Agg`).
- **Formatos numéricos**: Se asume formato USD. Ajusta `parse_financial_value()` si usas otra moneda.

## Depuración y pruebas rápidas

### Extracción de datos

```python
from src.client import MicrosoftIRClient
client = MicrosoftIRClient()
reports = client.get_annual_reports()
print(f"Encontrados {len(reports)} informes")
```

### Generación de tesis IA

```python
from src.gemini_ai import generate_financial_tesis
import json

# Cargar datos previamente extraídos
with open("downloads/all_ms_financial_data.json") as f:
    data = json.load(f)

tesis = generate_financial_tesis(data)
print(tesis)
```

### Visualización de gráficas

```python
from src.visualization import generate_tables
import json

with open("downloads/all_ms_financial_data.json") as f:
    data = json.load(f)

generate_tables(data)  # Muestra las dos gráficas
```

### Ejecutar tests

```powershell
pytest tests/ -v
```

## Cómo contribuir

Proceso para contribuir:

1. Fork del repositorio.
2. Crear una rama de feature: `git checkout -b feat/nombre-feature`.
3. Hacer PR con descripción clara y tests incluidos.

## Contacto y licencia

Si necesitas contactar al autor original, `juan.arabaolaza@gmail.com` (ver `pyproject.toml`).
