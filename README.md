# LAB-SEM-ML

**Digital Twin — Comunidad Residencial Inteligente para Generación de Series de Tiempo Multivariables Sintéticas y Analítica Energética Impulsada por IA**

![Version](https://img.shields.io/badge/version-1.0.0-indigo)
![Stack](https://img.shields.io/badge/stack-Python%20%7C%20FastAPI%20%7C%20Next.js%20%7C%20Three.js-6366f1)

---

## Tabla de Contenidos

1. [Descripción General](#descripción-general)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Sistema Multi-Agente](#sistema-multi-agente)
4. [Motor de Simulación](#motor-de-simulación)
5. [Variables Generadas (36 por registro)](#variables-generadas)
6. [Modelo Ambiental Posicional](#modelo-ambiental-posicional)
7. [Escenarios Experimentales](#escenarios-experimentales)
8. [Backend — API REST + WebSocket](#backend)
9. [Frontend — Visualización 3D + Dashboard](#frontend)
10. [Analítica y Machine Learning](#analítica-y-machine-learning)
11. [Almacenamiento de Datos](#almacenamiento-de-datos)
12. [Exportación de Datasets](#exportación-de-datasets)
13. [Despliegue](#despliegue)
14. [Estructura del Proyecto](#estructura-del-proyecto)
15. [Objetivos de Investigación](#objetivos-de-investigación)
16. [Créditos](#créditos)

---

## Descripción General

**LAB-SEM-ML** es una plataforma web completa que implementa un **Gemelo Digital (Digital Twin)** de una comunidad residencial compuesta por **2 torres**, **4 pisos cada una**, y **4 apartamentos por piso** — **32 apartamentos en total**.

Cada apartamento es un **agente inteligente autónomo** que simula el comportamiento de una familia real: horarios de sueño, trabajo, cocina, limpieza, entretenimiento, y consumo de servicios públicos. Un **Agente Ambiental** global genera condiciones climáticas coherentes usando componentes de Fourier, ruido Perlin y cadenas de Markov.

El resultado es un **dataset multivariable sintético** de alta resolución (minuto a minuto) con **36 variables por registro**, ideal para:

- Entrenamiento de modelos de IA
- Investigación en pronósticos (forecasting)
- Detección de anomalías
- Optimización energética
- Investigación en ciudades inteligentes
- Sistemas multi-agente
- Experimentos de aprendizaje por refuerzo
- Publicaciones académicas

---

## Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (Next.js)                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │   3D     │  │Dashboard │  │ Export   │  │Research  │ │
│  │  Scene   │  │          │  │ Center   │  │ Portal   │ │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘ │
│       └──────────────┼──────────────┼────────────┘       │
│                      │     React Query + WebSocket        │
├──────────────────────┼────────────────────────────────────┤
│              Backend (FastAPI — Python)                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │   MAS    │  │  Engine  │  │Analytics │  │   Data   │ │
│  │ Agents   │  │Simulation│  │  ML      │  │  Parquet │ │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘ │
│                      │                                    │
│              DuckDB + PyArrow + Polars                    │
└───────────────────────────────────────────────────────────┘
```

---

## Sistema Multi-Agente

### Jerarquía de Agentes

```
CommunityAgent (1)
├── EnvironmentAgent (1)
│   ├── Temperatura (Fourier + Perlin)
│   ├── Humedad (Ciclo diario + clima)
│   ├── Viento (Perfil logarítmico + ráfagas)
│   ├── Lluvia (Cadena Markov)
│   ├── Radiación Solar (Ángulo solar + nubosidad)
│   ├── Calidad del Aire
│   └── Presión Atmosférica
│
├── TowerAgent (2: A–B)
│   └── FloorAgent (4 por torre = 8)
│       └── ApartmentAgent (4 por piso = 32)
│           ├── Simulador Familiar
│           ├── Predictor de Ocupación
│           ├── Planificador de Actividades
│           ├── Modelo de Consumo
│           ├── Controlador de Batería
│           ├── Controlador Solar
│           └── Módulo de Memoria
```

### EnvironmentAgent

Genera variables ambientales usando:

- **Series de Fourier**: Temperatura y humedad diarias con armónicos
- **Ruido Perlin**: Micro-variaciones realistas
- **Cadena de Markov**: Transiciones climáticas (despejado → nublado → lluvioso)
- **Correlaciones cruzadas**: Temperatura ↑ → humedad cambia, radiación solar ↑ → temperatura ↑

### ApartmentAgent

Cada agente contiene una **máquina de estados** con 12 estados de actividad:

| Estado | Descripción |
|--------|-------------|
| `SLEEPING` | Todos durmiendo |
| `WAKING` | Despertar |
| `MORNING_ROUTINE` | Ducha, aseo |
| `AWAY` | Fuera de casa |
| `WORKING` | Trabajo remoto o presencial |
| `STUDYING` | Estudio |
| `COOKING` | Cocinar |
| `EATING` | Comer |
| `LEISURE` | Ocio |
| `CLEANING` | Limpieza |
| `NIGHT_ROUTINE` | Rutina nocturna |
| `ENTERTAINMENT` | Entretenimiento (TV, gaming) |

#### Perfil Familiar

Cada apartamento tiene un perfil único generado aleatoriamente:

- **Tamaño familiar**: 1–5 personas
- **Distribución de edades**: Niños, adolescentes, adultos, adultos mayores
- **Nivel de ingresos**: Bajo, medio, alto, premium
- **Conciencia sostenible**: 0.1–0.95
- **Trabajo remoto**: Depende del nivel de ingresos
- **Electrodomésticos**: Nevera, estufa, microondas, lavadora, TV, computador, AC, calentador, consola de juegos

#### Memoria del Agente

Cada agente almacena un historial de los últimos 90 días:

- Consumo diario de agua, electricidad y gas
- Facturas mensuales
- Historial de confort

**Comportamiento adaptativo**: Si las facturas superan un umbral, el agente activa el "modo ecológico":
- Reduce el uso del AC
- Apaga electrodomésticos innecesarios
- Desplaza consumo a horas valle

Si el confort baja demasiado, revierte parcialmente estas medidas.

---

## Motor de Simulación

### Tiempo Virtual

| Tiempo virtual | Tiempo real |
|---------------|-------------|
| 1 minuto | 0.5 segundos |
| 1 hora | 30 segundos |
| 1 día | 12 minutos |
| 30 días | 6 horas |

### Ciclo de Simulación

Por cada tick (0.5s reales):

1. **Environment Agent** calcula clima del minuto virtual → O(1)
2. **168 Apartment Agents** calculan su estado en paralelo → O(n)
3. **Community Agent** verifica comportamientos emergentes
4. **Persistencia** en buffer → lote cada 10 minutos virtuales → Parquet
5. **WebSocket** envía estados a los observadores (frontend)

### Control de Velocidad

El usuario puede ajustar la velocidad de 0.5× a 10×.

---

## Variables Generadas

Para cada apartamento, cada minuto virtual:

| # | Variable | Tipo | Descripción |
|---|----------|------|-------------|
| 1 | `timestamp` | uint64 | Minuto virtual |
| 2 | `apartment_id` | string | ID único (ej: `A2-3`) |
| 3 | `tower` | string | Torre (A–F) |
| 4 | `floor` | uint8 | Piso (1–7) |
| 5 | `apartment_number` | uint8 | Número (1–4) |
| 6 | `temperature` | float32 | Temperatura local (°C) |
| 7 | `humidity` | float32 | Humedad (%) |
| 8 | `wind_speed` | float32 | Velocidad del viento (m/s) |
| 9 | `rain` | float32 | Lluvia (mm) |
| 10 | `solar_radiation` | float32 | Radiación solar (W/m²) |
| 11 | `air_quality` | float32 | Calidad del aire (0–100) |
| 12 | `pressure` | float32 | Presión atmosférica (hPa) |
| 13 | `num_people_present` | uint8 | Personas presentes |
| 14 | `occupancy_state` | string | empty / partial / full |
| 15 | `activity_type` | string | Actividad actual |
| 16 | `water_liters` | float32 | Agua consumida (L) |
| 17 | `water_cost` | float32 | Costo del agua ($) |
| 18 | `electricity_wh` | float32 | Electricidad consumida (Wh) |
| 19 | `electricity_cost` | float32 | Costo electricidad ($) |
| 20 | `gas_m3` | float32 | Gas consumido (m³) |
| 21 | `gas_cost` | float32 | Costo del gas ($) |
| 22 | `internet_gb` | float32 | Internet usado (GB) |
| 23 | `internet_cost` | float32 | Costo internet ($) |
| 24 | `battery_charge` | float32 | Carga de batería (Wh) |
| 25 | `solar_generation` | float32 | Generación solar (Wh) |
| 26 | `comfort_score` | float32 | Puntaje confort (0–1) |
| 27 | `sustainability_score` | float32 | Puntaje sostenibilidad (0–1) |
| 28 | `scenario` | string | Escenario activo |

**Total**: 28 columnas en esquema Parquet (36 incluyendo las 8 de partición/derivadas)

**Volumen**: 32 aptos × 1440 min/día × 30 días = **1,382,400 registros/mes**

---

## Modelo Ambiental Posicional

Una de las características más importantes del simulador es que **la altura y la orientación de cada apartamento influyen directamente en su microclima**.

### Efecto de la Altura (Piso)

| Piso | Temperatura | Viento | Radiación Solar | Calidad del Aire |
|------|-------------|--------|-----------------|-------------------|
| 1–2 (bajos) | +0.3°C (calor del suelo) | 30% del viento base | 70% de la base (sombra) | −2 puntos |
| 3–5 (medios) | Neutro | 60% del viento base | 100% de la base | +3 puntos |
| 6–7 (altos) | −0.6°C (más viento) | 100% del viento base (perfil logarítmico) | 130% de la base (más sol directo) | +6 puntos |

El viento sigue un **perfil logarítmico**: `factor = ln(piso + 1) / ln(8)`, lo que significa que los pisos superiores reciben **mucho más viento** que los inferiores.

### Efecto de la Orientación (Número de Apartamento)

Cada torre está en una posición angular en el círculo de la comunidad, y cada apartamento mira hacia una dirección diferente:

| Apt | Orientación | Mañana (6–12h) | Mediodía (12–18h) | Tarde (18–21h) |
|-----|-------------|----------------|-------------------|-----------------|
| 1 | Noreste | ⬆️ Sol directo | ☁️ Sombra parcial | 🌑 Sombra |
| 2 | Sureste | ⬆️ Sol directo | ☀️ Sol alto | 🌑 Sombra |
| 3 | Suroeste | 🌑 Sombra | ☀️ Sol alto | ⬆️ Sol directo |
| 4 | Noroeste | 🌑 Sombra | ☁️ Sombra parcial | ⬆️ Sol directo |

La **dirección absoluta** se calcula como `ángulo de la torre + ángulo del apartamento`, y se compara con la **posición del sol** (que varía según la hora del día) para determinar la exposición solar real.

### Sombra entre Torres

Las torres se proyectan sombra entre sí. Con 2 torres enfrentadas (A al oeste, B al este), la Torre A proyecta sombra sobre la Torre B en la mañana y viceversa en la tarde.

### Impacto en el Consumo

Estos efectos posicionales impactan directamente:

- **Aire acondicionado**: Apartamentos con más sol (pisos altos, orientación soleada) usan más AC
- **Calefacción**: Apartamentos con más sombra o más viento (pisos altos) usan más calefacción en invierno
- **Generación solar**: Apartamentos con mejor orientación solar generan más electricidad
- **Confort**: La temperatura local afecta el puntaje de confort

---

## Escenarios Experimentales

El sistema incluye 7 escenarios predefinidos para experimentos académicos:

| Mes | Escenario | Descripción | Variable a Medir |
|-----|-----------|-------------|-------------------|
| 1 | **Baseline** | Comportamiento normal, sin intervenciones | Línea base |
| 2 | **Paneles Solares** | Instalación de paneles en todos los aptos | Reducción de consumo de red |
| 3 | **Baterías** | Baterías + paneles solares | Autosuficiencia energética |
| 4 | **Cortes Eléctricos** | Apagones programados de 1–2h | Resiliencia comunitaria |
| 5 | **Restricción de Agua** | Suministro reducido al 70% | Estrategias de adaptación |
| 6 | **Ola de Calor** | +8°C de temperatura extrema | Demanda de refrigeración |
| 7 | **Aumento de Precios** | Tarifas de servicios al triple | Elasticidad del consumo |

Además, se pueden crear **escenarios personalizados** dinámicamente a través de la API.

---

## Backend

### Tecnologías

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| Python | 3.11+ | Lenguaje principal |
| FastAPI | 0.110+ | Framework REST + WebSocket |
| DuckDB | 1.0+ | Base de datos analítica embebida |
| PyArrow | 15+ | Esquemas y lectura/escritura Parquet |
| Polars | 1.0+ | Procesamiento de datos tabulares |
| scikit-learn | 1.4+ | Clustering, anomalías |
| XGBoost | 2.0+ | Forecasting (disponible) |
| PyTorch | 2.2+ | LSTM/Transformer (disponible) |

### API REST

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| **Simulación** | | |
| POST | `/api/simulation/start` | Iniciar simulación |
| POST | `/api/simulation/pause` | Pausar |
| POST | `/api/simulation/resume` | Reanudar |
| POST | `/api/simulation/stop` | Detener |
| GET | `/api/simulation/status` | Estado actual |
| POST | `/api/simulation/scenario` | Crear escenario |
| GET | `/api/simulation/scenarios` | Listar escenarios |
| WS | `/api/simulation/stream` | WebSocket en tiempo real |
| **Comunidad** | | |
| GET | `/api/community/summary` | Estadísticas agregadas |
| GET | `/api/community/timeseries` | Series temporales |
| GET | `/api/community/sustainability` | KPIs de sostenibilidad |
| GET | `/api/community/emergence` | Comportamientos emergentes |
| **Torres** | | |
| GET | `/api/towers` | Listar torres |
| GET | `/api/towers/{id}` | Detalle de torre |
| GET | `/api/towers/{id}/timeseries` | Datos de torre |
| GET | `/api/towers/{id}/floors` | Pisos de la torre |
| **Apartamentos** | | |
| GET | `/api/apartments` | Listar (filtro torre/piso) |
| GET | `/api/apartments/{id}` | Detalle |
| GET | `/api/apartments/{id}/timeseries` | Serie temporal |
| GET | `/api/apartments/{id}/hourly` | Agregación horaria |
| GET | `/api/apartments/{id}/daily` | Agregación diaria |
| GET | `/api/apartments/{id}/realtime` | Estado en vivo |
| **Analítica** | | |
| GET | `/api/analytics/forecast/{id}` | Pronóstico |
| GET | `/api/analytics/anomalies/{id}` | Anomalías detectadas |
| GET | `/api/analytics/clusters` | Arquetipos de consumo |
| GET | `/api/analytics/recommendations/{id}` | Recomendaciones IA |
| GET | `/api/analytics/insights/{id}` | Reporte completo IA |
| **Exportación** | | |
| GET | `/api/export/apartment/{id}` | Descargar dataset |
| GET | `/api/export/tower/{id}` | Descargar torre |
| GET | `/api/export/community` | Descargar comunidad |

### WebSocket

El endpoint `ws://localhost:8000/api/simulation/stream` envía actualizaciones en tiempo real con el estado de todos los apartamentos cada tick de simulación.

---

## Frontend

### Tecnologías

| Tecnología | Propósito |
|------------|-----------|
| Next.js 14 | Framework React con App Router |
| TypeScript | Tipado estático |
| TailwindCSS | Estilos utilitarios |
| Three.js + React Three Fiber | Visualización 3D |
| @react-three/drei | Utilidades 3D (OrbitControls, Environment) |
| Zustand | Estado global del cliente |
| React Query | Estado del servidor + caché |
| Recharts | Gráficos (disponible) |
| Lucide React | Iconos |

### Visualización 3D

La escena 3D muestra:

- **6 torres** dispuestas en círculo, cada una con 7 pisos
- **168 apartamentos** como cajas individuales, **coloreadas por consumo**:
  - 🟢 Verde: consumo bajo (< 10 Wh)
  - 🟡 Amarillo: consumo medio (10–20 Wh)
  - 🔴 Rojo: consumo alto (> 20 Wh)
- **Efectos climáticos**: Partículas de lluvia/niebla
- **Etiquetas**: Nombre de cada torre con su arquetipo

**Interacción**:
- 🖱️ **Orbit**: Arrastrar para rotar, scroll para zoom
- 👆 **Click en apartamento**: Abre panel lateral con datos en tiempo real
- 🔍 **Hover**: Resalta el apartamento
- 🏢 **Click en torre**: Selecciona torre completa

### Panel Lateral

Al seleccionar un apartamento, se muestra:

- **Estado actual**: Actividad, ocupación, confort
- **Consumo en vivo**: Electricidad, agua, gas, internet (tarjetas)
- **Pestañas**:
  - **Info**: Variables ambientales y puntajes
  - **Charts**: Gráfico de pronóstico
  - **Analytics**: Anomalías, recomendaciones IA, pronóstico

### Dashboard

El dashboard comunitario incluye:

- **KPIs**: Total apartamentos, torres, confort promedio, sostenibilidad
- **Arquetipos de Torres**: Identidades emergentes (eficiente, moderada, alto consumo)
- **Perfiles de Consumo**: Clusters de residentes (Eco-Conscientes, Altos Consumidores, etc.)

### Páginas

| Ruta | Descripción |
|------|-------------|
| `/` | Vista 3D principal |
| `/dashboard` | Dashboard analítico completo |
| `/towers/{id}` | Detalle de torre con lista de apartamentos |
| `/apartments/{id}` | Detalle completo del apartamento |
| `/export` | Centro de descarga de datasets |
| `/research` | Portal de investigación con especificaciones |

---

## Analítica y Machine Learning

### Forecasting

Tres modelos disponibles (ensemble):

| Modelo | Horizonte | Uso |
|--------|-----------|-----|
| Regresión polinómica | 72 pasos | Tendencia rápida |
| XGBoost | 168 pasos | Features tabulares |
| LSTM (PyTorch) | 168 pasos | Secuencias temporales |
| Transformer (PyTorch) | 168 pasos | Patrones complejos |

### Detección de Anomalías

Métodos implementados:

- **Isolation Forest**: Por apartamento, ventana deslizante
- **Z-Score**: Desviación > 3σ sobre media móvil
- **Contextual**: Comparación con apartamentos similares del mismo cluster

### Clustering

Algoritmos para identificar arquetipos de consumo:

- **K-Means**: 4–6 arquetipos
- **DBSCAN**: Comunidades outlier
- **GMM**: Pertenencia probabilística

Features: `consumo eléctrico`, `agua`, `gas`, `horario pico`, `ratio noche`, `ratio fin de semana`, `conciencia sostenible`, `ingresos`, `tamaño familiar`

### Recomendaciones

Sistema híbrido (reglas + ML):

```
if electricidad > percentil 90:
    → "Actualizar electrodomésticos"
    → "Adoptar energía solar"
    → "Desplazar consumo a horas valle"

if agua > percentil 90:
    → "Instalar aireadores de bajo flujo"
    → "Revisar fugas"
    → "Captación de agua lluvia"
```

---

## Almacenamiento de Datos

### Esquema de Particionamiento (Hive)

```
data/
├── year=2026/
│   ├── month=01/
│   │   ├── day=01/
│   │   │   ├── batch_0000.parquet
│   │   │   ├── batch_0001.parquet
│   │   │   └── ...
│   │   ├── day=02/
│   │   └── ...
│   ├── month=02/
│   └── ...
```

### Compresión

- Formato: **Apache Parquet**
- Compresión: **Snappy**
- Tamaño estimado: ~40 MB por mes completo (~1.38M registros)

### Tablas Agregadas (Materializadas)

| Tabla | Granularidad | Columnas clave |
|-------|-------------|----------------|
| `hourly_aggregates` | Torre, piso, apto, hora | Suma consumo, promedio temperatura |
| `daily_aggregates` | Torre, piso, apto, día | Totales diarios, promedios |
| `monthly_aggregates` | Torre, apto, mes | Facturación mensual |

### Motor de Consulta

DuckDB permite consultas SQL directas sobre los archivos Parquet:

```sql
SELECT apartment_id, SUM(electricity_wh) as total_elec
FROM read_parquet('data/**/*.parquet', hive_partitioning=true)
WHERE tower = 'A' AND timestamp BETWEEN 10000 AND 20000
GROUP BY apartment_id
ORDER BY total_elec DESC;
```

---

## Exportación de Datasets

### Formatos Disponibles

| Formato | Uso Recomendado | Extensión |
|---------|-----------------|-----------|
| CSV | Herramientas de oficina, Excel | `.csv` |
| JSON | APIs, integraciones | `.json` |
| **Parquet** | **Investigación, ML, Big Data** | `.parquet` |

### Filtros de Exportación

- Por **apartamento**: `A2-3`
- Por **torre**: Todas las torres (A–F)
- Por **comunidad**: Dataset completo (168 aptos)
- Por **rango de fechas**: Ventana temporal específica
- Por **escenario**: Datos de un escenario particular

---

## Despliegue

### Local (Desarrollo)

**Backend**:
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**Frontend**:
```bash
cd frontend
npm install
npm run dev
```

### Docker Compose

```bash
docker-compose up --build
```

### Producción

| Componente | Servicio |
|------------|----------|
| Frontend | Vercel |
| Backend | Render / Fly.io |
| Datos | Cloudflare R2 / AWS S3 |

---

## Estructura del Proyecto

```
LAB-SEM-ML/
├── backend/                    # Backend Python
│   ├── app/
│   │   ├── main.py            # FastAPI entry point
│   │   ├── config.py          # Configuración central
│   │   ├── api/               # Rutas REST
│   │   │   ├── apartments.py
│   │   │   ├── towers.py
│   │   │   ├── simulation.py
│   │   │   ├── analytics.py
│   │   │   ├── community.py
│   │   │   └── export.py
│   │   ├── agents/            # Sistema Multi-Agente
│   │   │   ├── base_agent.py
│   │   │   ├── environment_agent.py
│   │   │   ├── apartment_agent.py
│   │   │   ├── community_agent.py
│   │   │   └── agent_scheduler.py
│   │   ├── simulation/        # Motor de simulación
│   │   │   └── engine.py
│   │   ├── models/            # Modelos de datos
│   │   │   ├── apartment.py
│   │   │   ├── environment.py
│   │   │   ├── scenarios.py
│   │   │   ├── tower.py
│   │   │   ├── community.py
│   │   │   ├── appliances.py
│   │   │   └── analytics.py
│   │   ├── data/              # Persistencia
│   │   │   ├── schema.py
│   │   │   ├── storage_manager.py
│   │   │   ├── query_engine.py
│   │   │   └── export_service.py
│   │   ├── analytics/         # ML/Analítica
│   │   │   ├── forecasting.py
│   │   │   ├── anomaly_detection.py
│   │   │   ├── clustering.py
│   │   │   └── recommender.py
│   │   └── utils/             # Utilidades
│   │       ├── fourier.py
│   │       ├── noise.py
│   │       ├── markov.py
│   │       ├── distributions.py
│   │       └── positional.py
│   ├── data/                  # Datos generados (Parquet)
│   ├── models/                # Modelos ML entrenados
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/                  # Frontend Next.js
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx           # Vista 3D principal
│   │   ├── dashboard/
│   │   ├── export/
│   │   ├── research/
│   │   ├── towers/[towerId]/
│   │   └── apartments/[apartmentId]/
│   ├── components/
│   │   ├── 3d/                # React Three Fiber
│   │   │   ├── Scene.tsx
│   │   │   ├── Community.tsx
│   │   │   ├── Tower.tsx
│   │   │   ├── Floor.tsx
│   │   │   ├── Apartment.tsx
│   │   │   ├── Ground.tsx
│   │   │   ├── WeatherFX.tsx
│   │   │   └── Labels.tsx
│   │   ├── dashboard/
│   │   ├── simulation/
│   │   └── ui/
│   ├── hooks/
│   │   ├── useSimulation.ts
│   │   └── useWebSocket.ts
│   ├── stores/
│   │   ├── simulationStore.ts
│   │   ├── selectionStore.ts
│   │   └── uiStore.ts
│   ├── lib/
│   │   ├── api.ts
│   │   ├── types.ts
│   │   └── constants.ts
│   ├── package.json
│   └── Dockerfile
│
├── docker-compose.yml
└── README.md
```

---

## Objetivos de Investigación

LAB-SEM-ML está diseñado para servir como plataforma de investigación en:

### 1. Generación de Datos Sintéticos Realistas

El sistema produce datos multivariables coherentes donde:

- Las variables ambientales siguen patrones físicos reales (Fourier, Perlin)
- El consumo energético emerge de actividades humanas simuladas, no de números aleatorios
- Los agentes aprenden y se adaptan basados en memoria (facturas pasadas)
- Emergen comportamientos comunitarios (torres eficientes vs. alto consumo)
- La posición y altura de cada apartamento afecta su microclima

### 2. Experimentos de Machine Learning

- **Forecasting**: Predecir demanda de electricidad, agua y gas
- **Anomaly Detection**: Detectar fugas, consumo anormal, fallos de equipos
- **Clustering**: Identificar perfiles de consumo y arquetipos de residentes
- **Reinforcement Learning**: Optimizar políticas de conservación energética

### 3. Investigación en Sistemas Multi-Agente

- Comportamientos emergentes a nivel comunidad
- Memoria y adaptación en agentes autónomos
- Interacciones entre agentes ambientales y de consumo

### 4. Ciudades Inteligentes

- Resiliencia ante cortes de energía
- Estrategias de adaptación a restricciones de agua
- Respuesta a olas de calor
- Elasticidad del consumo ante cambios de precios

---

## Créditos

**Semillero Machine Learning** — Laboratorio 1

Plataforma desarrollada como parte del semillero de investigación en Machine Learning, enfocada en la generación de datasets sintéticos multivariables para investigación académica en gemelos digitales, ciudades inteligentes y analítica energética.

---
*LAB-SEM-ML v1.0.0 — Digital Twin Smart Community*
