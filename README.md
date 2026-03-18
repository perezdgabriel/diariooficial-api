# Diario Oficial de Chile — API Normas Generales

API REST pública para consultar las normas generales (leyes, decretos y resoluciones de orden general) publicadas en el [Diario Oficial de Chile](https://www.diariooficial.interior.gob.cl/edicionelectronica/).

Los datos se recopilan diariamente mediante [diariooficial](https://github.com/perezdgabriel/diariooficial) y se almacenan en una base de datos Supabase.

## Endpoints

### `GET /normas`

Lista normas con filtros opcionales y paginación.

| Parámetro   | Tipo   | Descripción                                          |
|-------------|--------|------------------------------------------------------|
| `date_from` | date   | Filtrar desde esta fecha (inclusive, `YYYY-MM-DD`)    |
| `date_to`   | date   | Filtrar hasta esta fecha (inclusive, `YYYY-MM-DD`)    |
| `ministry`  | string | Búsqueda parcial por ministerio (no distingue mayúsculas) |
| `branch`    | string | Filtrar por poder (ej. `PODER EJECUTIVO`)             |
| `search`    | string | Búsqueda en el título de la norma                     |
| `offset`    | int    | Offset de paginación (por defecto `0`)                |
| `limit`     | int    | Resultados por página (por defecto `50`, máx `500`)   |

### `GET /normas/{cve}`

Obtener una norma por su código CVE (Código de Verificación Electrónica).

### `GET /normas/dates/available`

Lista las fechas que tienen normas publicadas, de la más reciente a la más antigua.

### `GET /normas/stats/by-ministry`

Cantidad de normas agrupadas por ministerio, con filtro opcional por rango de fechas (`date_from`, `date_to`).

## Ejecución local

```bash
# Crear archivo .env
echo "SUPABASE_URL=https://tu-proyecto.supabase.co" >> .env
echo "SUPABASE_ANON_KEY=tu-anon-key" >> .env

# Instalar dependencias y ejecutar
pip install -r requirements.txt
uvicorn main:app --reload
```

Documentación interactiva disponible en [http://localhost:8000/docs](http://localhost:8000/docs).

## Docker

```bash
docker build -t diariooficial-api .
docker run -p 8000:8000 \
  -e SUPABASE_URL=https://tu-proyecto.supabase.co \
  -e SUPABASE_ANON_KEY=tu-anon-key \
  diariooficial-api
```

## Modelo de datos

Cada norma contiene:

| Campo      | Descripción                                              |
|------------|----------------------------------------------------------|
| `id`       | Clave primaria autoincremental                           |
| `date`     | Fecha de publicación                                     |
| `edition`  | Número de edición (ej. `Edición Núm. 44.398.`)          |
| `branch`   | Poder del Estado (`PODER EJECUTIVO`, `OTRAS ENTIDADES`)  |
| `ministry` | Nombre del ministerio                                    |
| `organ`    | Subsecretaría o servicio                                 |
| `title`    | Título completo de la norma                              |
| `pdf_url`  | Enlace directo al PDF oficial                            |
| `cve`      | Código de Verificación Electrónica (único)               |
