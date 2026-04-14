# PRD CUBA DIGEST v2.0 — COMPLETO Y LISTO PARA IMPLEMENTACIÓN

**Versión:** 2.0  
**Fecha:** 2026-04-12  
**Estado:** Ready for Implementation  
**Plataforma:** Claude Code + Python  
**Optimizado por:** ARCHIE v1.1  

---

## ÍNDICE

1. [Resumen Ejecutivo](#1-resumen-ejecutivo)
2. [Problema](#2-problema)
3. [Objetivo del Producto](#3-objetivo-del-producto)
4. [Usuarios](#4-usuarios)
5. [Posicionamiento Editorial](#5-posicionamiento-editorial)
6. **[NUEVO] Estrategia de IA y Enriquecimiento**
7. [Fuentes](#7-fuentes)
8. [Unidad Principal del Sistema](#8-unidad-principal-del-sistema)
9. [Experiencia de Usuario](#9-experiencia-de-usuario)
10. **[NUEVO] Algoritmos de Procesamiento**
11. **[NUEVO] Configuración del Sistema**
12. [Política de Contenido y Copyright](#12-política-de-contenido-y-copyright)
13. [Arquitectura Técnica](#13-arquitectura-técnica)
14. **[NUEVO] Estrategia de Testing y Validación**
15. [MVP Shareable](#15-mvp-shareable)
16. [Métricas de Éxito](#16-métricas-de-éxito)
17. [Riesgos](#17-riesgos)
18. [Roadmap de Implementación](#18-roadmap-de-implementación)
19. **[NUEVO] Artifacts de Implementación**

---

## 1. RESUMEN EJECUTIVO

### Nombre del Producto
**Cuba Digest**

### Tipo de Producto
Sistema de curación, síntesis y lectura estructurada sobre noticias de Cuba

### Objetivo Primario
Permitir a un usuario consumir rápidamente, con contexto y con confianza, lo más relevante sobre Cuba sin tener que revisar múltiples canales, medios y narrativas por separado.

### Usuario Inicial
- Esposa del fundador
- Círculo cercano de familia/amigos
- 10-15 testers iniciales

### Hipótesis de Expansión
Producto compartible que puede evolucionar hacia servicio para comunidad cubana y diáspora.

### Propuesta de Valor Principal

Cuba Digest **NO ES**:
- ❌ Un agregador de noticias
- ❌ Un simple resumen automático
- ❌ Un bot de RSS

Cuba Digest **ES**:
- ✅ Un reader inteligente multi-vista
- ✅ Un sistema curado con criterio editorial
- ✅ Una herramienta de síntesis narrativa
- ✅ Un organizador de panorama informativo

**Diferenciadores clave:**
1. Prioriza medios independientes y de la diáspora
2. Separa claramente la cobertura estatal
3. Organiza información por tema, medio, video, trending y contexto internacional
4. Sintetiza narrativas sin copiar contenido
5. Enlaza siempre a las fuentes originales

---

## 2. PROBLEMA

### 2.1 Fragmentación
El usuario interesado en noticias sobre Cuba enfrenta información distribuida entre:
- Canales de YouTube
- Medios independientes
- Medios de la diáspora
- Medios internacionales
- Medios estatales

**Resultado:** Consumir el panorama completo requiere visitar 10+ fuentes diferentes.

### 2.2 Ruido
Exceso de:
- Contenido repetido (mismo cable de AP en 5 medios)
- Clickbait sin sustancia
- Opinión sin fundamento
- Propaganda estatal poco útil
- Videos largos donde el valor tarda en aparecer

**Resultado:** 80% del tiempo se gasta en filtrar, no en aprender.

### 2.3 Falta de Síntesis
Aunque haya múltiples coberturas de un mismo evento, el usuario debe:
- Detectarlo manualmente
- Comparar versiones
- Entender qué es realmente importante
- Construir mentalmente el panorama

**Resultado:** Carga cognitiva alta para entender "qué está pasando realmente".

### 2.4 Falta de Confianza
En el contexto cubano hay alto nivel de desconfianza hacia las fuentes.

**Por eso no basta con resumir:** el sistema debe ser transparente, trazable y verificable.

---

## 3. OBJETIVO DEL PRODUCTO

Construir un sistema que:

1. ✅ Recolecte noticias relevantes sobre Cuba desde YouTube y medios digitales
2. ✅ Filtre ruido y baje prioridad a lo irrelevante
3. ✅ Agrupe el contenido por temas/narrativas
4. ✅ Muestre al usuario distintas vistas del mismo dataset
5. ✅ Enlace siempre a la fuente original
6. ✅ Permita ver la cobertura estatal solo si el usuario lo desea
7. ✅ Sea compartible en un MVP estático para validación temprana

---

## 4. USUARIOS

### 4.1 Usuario Principal

**Perfil:**
- Sigue noticias sobre Cuba con frecuencia
- Consume YouTube y medios digitales
- Quiere reducir tiempo de consumo
- Valora claridad y orden
- No quiere ruido
- Quiere poder verificar la fuente original

**Comportamiento actual:**
- Revisa 5-10 fuentes/día
- Gasta 60-90 minutos en consumo de noticias
- Frustración por contenido repetido

**Comportamiento deseado:**
- Revisa 1 digest/día
- Gasta 15-20 minutos
- Alta confianza en panorama completo

### 4.2 Usuarios Secundarios
- Amigos y familia del fundador
- Miembros de la diáspora
- Usuarios con interés en cobertura más estructurada y crítica de Cuba

### 4.3 Usuario Futuro
- Comunidad cubana en el exterior
- Lectores interesados en un producto editorial curado
- Académicos y analistas de Cuba

---

## 5. POSICIONAMIENTO EDITORIAL

### 5.1 Definición

**Cuba Digest es un sistema curado con criterio, NO neutral.**

Esto significa:
- ✅ Prioriza medios independientes y de la diáspora
- ✅ Da espacio al contexto internacional
- ✅ NO incorpora la cobertura estatal dentro del flujo principal
- ✅ Mantiene transparencia en la clasificación de fuentes

### 5.2 Lo que SÍ hace
- Síntesis
- Organización
- Priorización
- Contextualización ligera
- Narrativa por tema

### 5.3 Lo que NO hace
- Militancia explícita
- Propaganda
- Copia de contenido
- Opinión editorial fuerte escrita por el sistema

**El sistema interpreta, pero no opina.**

### 5.4 Principios Editoriales

1. **La fuente siempre visible**
2. **El enlace original siempre disponible**
3. **No copiar contenido completo**
4. **La cobertura estatal siempre separada**
5. **La vista por temas es la principal**
6. **La amplitud de cobertura importa:** no limitar artificialmente las fuentes top
7. **La síntesis debe ayudar a entender el panorama, no reemplazar la verificación**

---

## 6. ESTRATEGIA DE IA Y ENRIQUECIMIENTO

### 6.1 Modelo Primario

**Claude 3 Haiku**

**Razones:**
- ✅ Costo-efectivo para procesamiento diario (~$10/mes)
- ✅ Velocidad alta para pipeline batch
- ✅ Calidad suficiente para síntesis objetiva
- ✅ Contexto de 200K tokens (suficiente para clustering)

**Presupuesto estimado:**
```
50 items/día × 800 tokens promedio = 40,000 tokens/día
40,000 tokens/día × 30 días = 1.2M tokens/mes

Costo Haiku:
- Input: $0.25 / 1M tokens
- Output: $1.25 / 1M tokens

Estimado mensual: $8-12
```

### 6.2 Estrategia de Prompts

#### 6.2.1 Item Summary Prompt

**Objetivo:** Generar resumen objetivo de 5-8 líneas por item.

**Template:**
```xml
<sistema>
Eres un asistente editorial para Cuba Digest, un servicio de curación de noticias sobre Cuba.
Tu rol: generar resúmenes objetivos, descriptivos y concisos.

Principios:
- Objetividad descriptiva (reportar hechos, no opinar)
- Claridad y precisión
- Español neutro
- No copiar frases literales del original
- Máximo 150 palabras
</sistema>

<contexto_fuente>
Tipo: {tipo_contenido}
Medio: {nombre_medio}
Clasificación: {tier_editorial}
</contexto_fuente>

<contenido_original>
Título: {titulo}
Descripción: {descripcion}
{captions_preview si disponible}
</contenido_original>

<tarea>
Genera un resumen de 5-8 líneas que responda:
- ¿Qué ocurrió/se reporta?
- ¿Quién está involucrado?
- ¿Cuándo y dónde?
- ¿Por qué es relevante?

Formato: párrafo corrido, sin bullets.
</tarea>
```

**Ejemplo de output esperado:**
```
El Ministerio de Salud Pública de Cuba reportó un brote de dengue en la 
provincia de Santiago de Cuba, con más de 200 casos confirmados en las 
últimas dos semanas. Las autoridades implementaron fumigaciones intensivas 
en zonas urbanas y rurales. Medios independientes señalan que el número 
real podría ser mayor debido a subregistro. Esta situación coincide con 
escasez de repelentes y medicamentos en farmacias de la región.
```

#### 6.2.2 Item Insight Prompt

**Objetivo:** Generar insight breve (1-2 líneas) sobre qué agrega este item.

**Template:**
```xml
<sistema>
Genera un insight editorial breve sobre este contenido.

Principios:
- Máximo 50 palabras
- Indica qué aporta esta pieza al panorama
- Mantén tono analítico, no sensacionalista
</sistema>

<item>
Resumen: {resumen_generado}
Fuente: {medio} ({tier})
Fecha: {fecha}
</item>

<contexto_dia>
Otros items del día sobre temas relacionados:
{lista_items_relacionados}
</contexto_dia>

<tarea>
Responde brevemente:
- ¿Qué ángulo único ofrece esta fuente?
- ¿Qué agrega al entendimiento del tema?
- ¿Por qué importa en el contexto del día?
</tarea>
```

**Ejemplo de output esperado:**
```
Aporta datos oficiales sobre el brote, aunque medios independientes sugieren 
cifras mayores. Importante por contexto de crisis sanitaria y escasez de medicamentos.
```

#### 6.2.3 Topic Synthesis Prompt

**Objetivo:** Generar síntesis narrativa de un tema que agrupa múltiples items.

**Template:**
```xml
<sistema>
Eres un editor senior sintetizando múltiples coberturas sobre un mismo tema.

Principios:
- Objetividad narrativa
- Integrar perspectivas de múltiples fuentes
- Señalar consensos y divergencias
- Máximo 300 palabras
- Español claro y periodístico
</sistema>

<items_agrupados>
{lista de items con: medio, tier, resumen, fecha}
</items_agrupados>

<tarea>
Genera una síntesis narrativa que:
1. Explique qué está ocurriendo (el evento/situación central)
2. Por qué varias fuentes lo están cubriendo
3. Qué puntos hay en común entre las coberturas
4. Qué divergencias o ángulos únicos aporta cada fuente
5. Por qué esto importa en el contexto cubano actual

Formato: 2-3 párrafos, tono analítico pero accesible.
NO emitir opinión personal del sistema.
Separar hechos de interpretaciones cuando las haya.
</tarea>
```

**Ejemplo de output esperado:**
```
El gobierno cubano anunció nuevas medidas económicas que incluyen la 
liberalización parcial de precios en sectores no estratégicos y la 
apertura a más inversión privada en servicios. Según fuentes oficiales, 
estas reformas buscan estimular la producción nacional y reducir la 
dependencia de importaciones.

Medios independientes coinciden en reportar las medidas pero divergen 
en su interpretación: mientras Diario de Cuba las considera insuficientes 
y tardías, 14ymedio destaca que representan el cambio más significativo 
en política económica desde 2021. El Nuevo Herald contextualiza estas 
reformas en el marco de presiones internacionales y crisis energética.

La cobertura internacional, liderada por Reuters y AP, enfatiza el 
escepticismo de economistas sobre la capacidad de implementación dada 
la estructura burocrática actual. Todos los medios coinciden en que el 
impacto real dependerá de la ejecución y velocidad de implementación.
```

#### 6.2.4 Topic Naming Prompt

**Objetivo:** Generar nombre conciso para un tema.

**Template:**
```xml
<sistema>
Genera un título descriptivo para un tema que agrupa múltiples noticias.

Principios:
- Máximo 8 palabras
- Descriptivo, no sensacionalista
- Que capture la esencia del tema
- Sin verbos en infinitivo o gerundio
</sistema>

<sintesis_tema>
{síntesis narrativa generada}
</sintesis_tema>

<items_incluidos>
{títulos de items agrupados}
</items_incluidos>

<tarea>
Genera un título que funcione como nombre del tema.

Ejemplos de buenos títulos:
- "Nuevas medidas económicas y reacciones"
- "Brote de dengue en Santiago de Cuba"
- "Apagones y crisis energética"
- "Detención de activistas en La Habana"

Evitar:
- Títulos vagos: "Situación en Cuba"
- Títulos sensacionalistas: "¡Crisis total!"
- Títulos con gerundio: "Anunciando nuevas medidas"
</tarea>
```

### 6.3 Estrategia de Captions de YouTube

**Decisión:** Extraer primeros 500 caracteres como contexto adicional.

**Implementación:**
```python
def extract_youtube_context(video_id):
    """
    Extrae metadata + preview de captions para enriquecer contexto.
    """
    metadata = get_video_metadata(video_id)  # título, descripción, stats
    
    context = {
        'title': metadata['title'],
        'description': metadata['description'][:200],  # Primeros 200 chars
        'channel': metadata['channel_name'],
        'upload_date': metadata['upload_date'],
        'view_count': metadata['view_count'],
        'url': f"https://youtube.com/watch?v={video_id}"
    }
    
    # Intentar extraer captions automáticas
    try:
        captions = get_auto_captions(video_id)
        if captions:
            context['captions_preview'] = captions[:500]  # Primeros 500 chars
            context['has_captions'] = True
        else:
            context['has_captions'] = False
    except Exception as e:
        context['has_captions'] = False
        context['captions_error'] = str(e)
    
    return context
```

**Ratio esperado:**
- 80% videos tendrán captions automáticas
- 20% solo tendrán metadata (título + descripción)

**Beneficio:**
- Calidad de resumen aumenta ~25% con captions
- Permite distinguir videos con contenido real vs. clickbait puro

---

## 7. FUENTES

### 7.1 YouTube Channels

**Canales iniciales:**

| Canal | ID | Tier | Peso |
|-------|-------|------|------|
| Juan Manuel Cao | UCxxx | diáspora | 1.0 |
| Mario Pentón | UCxxx | diáspora | 1.0 |
| Martí Noticias | UCxxx | independiente | 1.0 |
| CiberCuba | UCxxx | independiente | 0.9 |
| Pepe Forte | UCxxx | diáspora | 0.8 |
| Abraham Rivera | UCxxx | diáspora | 0.8 |
| Rolando Nápoles | UCxxx | diáspora | 0.7 |
| Otaola | UCxxx | diáspora | 0.6 |
| Carlitos Madrid | UCxxx | diáspora | 0.6 |
| El Canal de las Emociones | UCxxx | diáspora | 0.5 |
| 23 y Flagged | UCxxx | independiente | 0.7 |
| Daniel Benítez | UCxxx | independiente | 0.7 |

**Nota:** Los IDs reales deben obtenerse de YouTube.

**Rol de YouTube:**
- Fuente secundaria, complementando medios escritos
- Aporta: contexto, interpretación, cobertura rápida, señales de engagement

### 7.2 Medios Digitales (RSS/Web)

**Medios iniciales:**

| Medio | URL RSS | Tier | Peso |
|-------|---------|------|------|
| CiberCuba | https://cibercuba.com/rss | independiente | 1.0 |
| Diario de Cuba | https://diariodecuba.com/rss | independiente | 1.0 |
| Cubanet | https://cubanet.org/feed/ | independiente | 1.0 |
| ADN Cuba | https://adncuba.com/rss | independiente | 0.9 |
| 14ymedio | https://14ymedio.com/feed/ | independiente | 1.0 |
| El Toque | https://eltoque.com/rss | independiente | 0.9 |
| El Nuevo Herald | https://elnuevoherald.com/rss | diáspora | 0.9 |
| Martí Noticias | https://martinoticias.com/rss | independiente | 1.0 |

### 7.3 Clasificación de Fuentes

Cada fuente debe tener una clasificación editorial:

- **independiente:** Medios independientes con base en Cuba o producidos por cubanos
- **diáspora:** Medios de cubanos en el exterior
- **internacional:** Medios internacionales que cubren Cuba (Reuters, AP, BBC, etc.)
- **estatal:** Medios controlados por el gobierno cubano (Granma, Cubadebate, etc.)

### 7.4 Cobertura Estatal

**Fuentes estatales a considerar (SOLO si toggle activado):**
- Granma
- Cubadebate
- Juventud Rebelde
- Canal estatal YouTube

**Comportamiento:**
- OFF por defecto
- Requiere activación explícita del usuario
- Nunca mezclada en el core
- Siempre etiquetada claramente

---

## 8. UNIDAD PRINCIPAL DEL SISTEMA

### 8.1 Item Enriquecido

**La unidad atómica del sistema.**

**Estructura:**
```json
{
  "id": "item_20260412_001",
  "type": "article",  // o "video"
  "source": {
    "name": "Diario de Cuba",
    "tier": "independiente",
    "url": "https://diariodecuba.com"
  },
  "content": {
    "title": "Título original del artículo/video",
    "url": "https://...",
    "published_date": "2026-04-12T10:30:00Z",
    "description": "Descripción original (si existe)"
  },
  "enrichment": {
    "summary": "Resumen generado por IA (5-8 líneas)",
    "insight": "Insight editorial breve (1-2 líneas)",
    "keywords": ["palabra1", "palabra2", "palabra3"]
  },
  "metadata": {
    "view_count": 12500,  // si es video
    "comment_count": 45,  // si disponible
    "has_captions": true  // si es video
  },
  "processing": {
    "collected_at": "2026-04-12T11:00:00Z",
    "enriched_at": "2026-04-12T11:05:00Z",
    "topic_assigned": "topic_20260412_economia"
  },
  "scoring": {
    "editorial_score": 0.9,
    "engagement_score": 0.7,
    "recency_score": 1.0,
    "source_tier_score": 1.0,
    "total_score": 0.875
  }
}
```

### 8.2 Tema (Topic)

**La unidad narrativa del sistema.**

Un tema agrupa múltiples items relacionados y produce:

**Estructura:**
```json
{
  "id": "topic_20260412_economia",
  "name": "Nuevas medidas económicas y reacciones",
  "created_at": "2026-04-12T11:15:00Z",
  "synthesis": {
    "narrative": "Síntesis narrativa del tema (2-3 párrafos)",
    "key_points": [
      "Punto clave 1",
      "Punto clave 2",
      "Punto clave 3"
    ]
  },
  "items": {
    "featured": ["item_001", "item_004", "item_007"],  // Destacados
    "additional": ["item_002", "item_003", "item_005"],  // Cobertura adicional
    "videos": ["item_009", "item_012"],  // Videos relacionados
    "state_coverage": ["item_020", "item_021"]  // Cobertura estatal (opcional)
  },
  "coverage": {
    "total_items": 12,
    "independiente": 6,
    "diaspora": 4,
    "internacional": 2,
    "estatal": 2
  },
  "scoring": {
    "importance_score": 0.95,
    "coverage_breadth": 0.85,
    "total_score": 0.90
  }
}
```

---

## 9. EXPERIENCIA DE USUARIO

### 9.1 Landing MVP

**URL:** `cubadigest.com` (o dominio temporal para testing)

**Objetivo:** Explicar el producto de forma simple antes de mostrar el digest.

**Estructura:**

```
┌─────────────────────────────────────┐
│         CUBA DIGEST                 │
│   Tu panorama diario sobre Cuba     │
├─────────────────────────────────────┤
│                                     │
│  🎯 ¿Qué es Cuba Digest?            │
│                                     │
│  No es otro agregador de noticias.  │
│  Es tu reader inteligente que:      │
│                                     │
│  ✓ Prioriza medios independientes   │
│  ✓ Organiza por temas, no por caos │
│  ✓ Sintetiza sin copiar             │
│  ✓ Separa cobertura estatal         │
│  ✓ Siempre enlaza al original       │
│                                     │
│  ─────────────────────────────────  │
│                                     │
│  📰 Fuentes que priorizamos:        │
│  • Diario de Cuba                   │
│  • 14ymedio                         │
│  • CiberCuba                        │
│  • Martí Noticias                   │
│  • El Nuevo Herald                  │
│  • + medios independientes          │
│                                     │
│  ─────────────────────────────────  │
│                                     │
│  🔒 Tratamiento de cobertura        │
│      estatal                        │
│                                     │
│  La cobertura de medios estatales   │
│  está separada y OFF por defecto.   │
│  Tú decides si quieres verla.       │
│                                     │
│  ─────────────────────────────────  │
│                                     │
│  [ Ver Digest de Hoy → ]            │
│                                     │
└─────────────────────────────────────┘
```

### 9.2 Digest HTML

**El digest funciona como reader inteligente multi-vista.**

#### Header

```
┌─────────────────────────────────────────────┐
│  CUBA DIGEST                    📅 12 Abr   │
│                                             │
│  Mostrar cobertura estatal  [⚪ OFF]       │
└─────────────────────────────────────────────┘
```

#### Hero: Core del Día

**Componente más prominente.**

```
┌─────────────────────────────────────────────┐
│  🔥 CORE DEL DÍA                            │
├─────────────────────────────────────────────┤
│                                             │
│  Hoy en Cuba:                               │
│                                             │
│  • Nuevas medidas económicas generan        │
│    reacciones mixtas                        │
│                                             │
│  • Brote de dengue en Santiago con más      │
│    de 200 casos                             │
│                                             │
│  • Apagones se extienden a 12 horas en      │
│    provincias del oriente                   │
│                                             │
│  • Detención de activista independiente     │
│    genera condenas internacionales          │
│                                             │
└─────────────────────────────────────────────┘
```

### 9.3 Tabs de Navegación

```
┌──────────────────────────────────────────┐
│ [TEMAS] Medios | Videos | Trending |    │
│                           Cuba Global     │
└──────────────────────────────────────────┘
```

#### Tab 1: TEMAS (Default)

**Vista principal del sistema.**

**Función:**
- Mostrar el panorama por narrativa
- Agrupar múltiples fuentes sobre un mismo tema
- Permitir profundización

**Estructura por tema:**

```
┌────────────────────────────────────────────────┐
│ 📌 Nuevas medidas económicas y reacciones      │
├────────────────────────────────────────────────┤
│                                                │
│ [Síntesis Narrativa - 2-3 párrafos]           │
│                                                │
│ El gobierno cubano anunció nuevas medidas...  │
│ ...                                            │
│                                                │
│ ────────────────────────────────────────────  │
│                                                │
│ 📰 Destacados                                  │
│                                                │
│ • "Gobierno anuncia liberalización de..."     │
│   Diario de Cuba • hace 2h                     │
│   [Resumen de 3 líneas]                        │
│   → Leer original                              │
│                                                │
│ • "Economistas dudan de la efectividad..."    │
│   14ymedio • hace 4h                           │
│   [Resumen de 3 líneas]                        │
│   → Leer original                              │
│                                                │
│ ────────────────────────────────────────────  │
│                                                │
│ 📄 Más cobertura (6 items)                     │
│                                                │
│ • CiberCuba • "Reformas económicas: qué..."   │
│ • El Toque • "Análisis: Medidas vs realidad"  │
│ • Cubanet • "Reacciones divididas ante..."    │
│ [+ Ver 3 más]                                  │
│                                                │
│ ────────────────────────────────────────────  │
│                                                │
│ 🎥 Videos relacionados (2)                     │
│                                                │
│ • "Mario Pentón analiza las reformas"         │
│   15K views • hace 3h                          │
│                                                │
│ • "Juan Manuel Cao: ¿Qué cambia realmente?"   │
│   8K views • hace 5h                           │
│                                                │
│ ────────────────────────────────────────────  │
│                                                │
│ 🏛️ Cobertura estatal (2)  [TOGGLE ON]         │
│                                                │
│ ⚠️ Narrativa de medios estatales.             │
│    Recomendamos contrastar.                    │
│                                                │
│ • Granma • "Medidas fortalecen economía..."   │
│ • Cubadebate • "Pueblo respalda reformas"     │
│                                                │
└────────────────────────────────────────────────┘
```

**Orden de temas:**
1. Score de importancia (combinado)
2. Número de items (mayor cobertura = más importante)
3. Recency

#### Tab 2: MEDIOS

**Agrupa por fuente.**

**Orden de medios:**
1. Independientes (alfabético)
2. Diáspora (alfabético)
3. Internacionales (alfabético)
4. Estatales (si toggle ON)

**Orden interno por medio:**
- Cronológico inverso (más reciente primero)

**Estructura:**

```
┌────────────────────────────────────────────────┐
│ 🏢 MEDIOS                                      │
├────────────────────────────────────────────────┤
│                                                │
│ 📰 INDEPENDIENTES                              │
│                                                │
│ ▼ 14ymedio (4 items)                           │
│   • "Economistas dudan de..." • hace 4h        │
│   • "Familias reportan apagones..." • hace 6h  │
│   • "Activista detenido en..." • hace 8h       │
│   [+ 1 más]                                    │
│                                                │
│ ▼ CiberCuba (3 items)                          │
│   • "Reformas económicas: qué..." • hace 2h    │
│   • "Dengue en Santiago: cifras..." • hace 5h  │
│   [+ 1 más]                                    │
│                                                │
│ ▼ Diario de Cuba (5 items)                     │
│   ...                                          │
│                                                │
│ ────────────────────────────────────────────  │
│                                                │
│ 🌎 DIÁSPORA                                    │
│                                                │
│ ▼ El Nuevo Herald (2 items)                    │
│   ...                                          │
│                                                │
│ ────────────────────────────────────────────  │
│                                                │
│ 🌐 INTERNACIONALES                             │
│                                                │
│ ▼ Reuters (1 item)                             │
│   ...                                          │
│                                                │
│ ────────────────────────────────────────────  │
│                                                │
│ 🏛️ ESTATALES  [TOGGLE ON]                     │
│                                                │
│ ⚠️ Medios controlados por el gobierno.        │
│                                                │
│ ▼ Granma (3 items)                             │
│   ...                                          │
│                                                │
└────────────────────────────────────────────────┘
```

#### Tab 3: VIDEOS

**Muestra solo contenido YouTube.**

**Orden:**
1. Score combinado (engagement + relevance + recency)
2. Fallback: cronológico inverso

**Estructura:**

```
┌────────────────────────────────────────────────┐
│ 🎥 VIDEOS                                      │
├────────────────────────────────────────────────┤
│                                                │
│ 🔥 Más relevantes hoy                          │
│                                                │
│ ▶ "Mario Pentón analiza las reformas"         │
│   Mario Pentón • 15K views • hace 3h           │
│   [Thumbnail]                                  │
│   [Resumen de 2-3 líneas]                      │
│   Insight: Aporta contexto económico...        │
│   → Ver video                                  │
│                                                │
│ ▶ "Juan Manuel Cao: ¿Qué cambia realmente?"   │
│   Juan Manuel Cao • 8K views • hace 5h         │
│   [Thumbnail]                                  │
│   [Resumen de 2-3 líneas]                      │
│   Insight: Perspectiva política...             │
│   → Ver video                                  │
│                                                │
│ ────────────────────────────────────────────  │
│                                                │
│ 📺 Todos los videos (12)                       │
│                                                │
│ ▶ Abraham Rivera • 5K views • hace 6h          │
│ ▶ Pepe Forte • 3K views • hace 8h              │
│ ▶ Rolando Nápoles • 2K views • hace 10h        │
│ [+ Ver más]                                    │
│                                                │
└────────────────────────────────────────────────┘
```

#### Tab 4: TRENDING

**Muestra:**
- Más vistos (YouTube)
- Más comentados
- Más relevantes del día

**Orden:**
- Engagement metrics + recency

**Estructura:**

```
┌────────────────────────────────────────────────┐
│ 🔥 TRENDING                                    │
├────────────────────────────────────────────────┤
│                                                │
│ 📊 Lo más visto hoy                            │
│                                                │
│ 1. 🎥 "Mario Pentón: Reformas económicas"      │
│    15K views • hace 3h                         │
│                                                │
│ 2. 📰 "Dengue en Santiago: crisis sanitaria"   │
│    Diario de Cuba • Alto engagement            │
│                                                │
│ 3. 🎥 "Juan Manuel Cao análisis político"      │
│    8K views • hace 5h                          │
│                                                │
│ 4. 📰 "Apagones extendidos en oriente"         │
│    14ymedio • Alto tráfico                     │
│                                                │
│ 5. 🎥 "Otaola reacciona a detenciones"         │
│    12K views • hace 4h                         │
│                                                │
│ ────────────────────────────────────────────  │
│                                                │
│ 💬 Más comentados                              │
│                                                │
│ • "Familias reportan 12h sin luz" • 156        │
│   CiberCuba                                    │
│                                                │
│ • "Economistas dudan de reformas" • 89         │
│   14ymedio                                     │
│                                                │
└────────────────────────────────────────────────┘
```

#### Tab 5: CUBA GLOBAL

**Vista específica para contexto internacional relacionado con Cuba.**

**Función:**
- Mostrar cómo Cuba aparece en medios internacionales
- Aportar contraste narrativo
- Ampliar contexto

**Fuentes:**
- Reuters
- Associated Press
- BBC
- The New York Times
- The Washington Post
- El País
- Otros medios internacionales

**Estructura:**

```
┌────────────────────────────────────────────────┐
│ 🌐 CUBA GLOBAL                                 │
├────────────────────────────────────────────────┤
│                                                │
│ Cuba en el contexto internacional              │
│                                                │
│ 🌍 Cobertura internacional                     │
│                                                │
│ 📰 Reuters • hace 2h                           │
│ "Cuba announces economic reforms amid crisis"  │
│ [Resumen]                                      │
│ Insight: Enfatiza escepticismo internacional   │
│ → Read original                                │
│                                                │
│ 📰 AP News • hace 5h                           │
│ "Dengue outbreak strains Cuban healthcare"    │
│ [Resumen]                                      │
│ Insight: Contextualiza crisis sanitaria...     │
│ → Read original                                │
│                                                │
│ 📰 BBC Mundo • hace 8h                         │
│ "Cuba: Los apagones y el descontento"         │
│ [Resumen]                                      │
│ Insight: Perspectiva europea sobre crisis...   │
│ → Leer original                                │
│                                                │
│ ────────────────────────────────────────────  │
│                                                │
│ 🗣️ Declaraciones internacionales               │
│                                                │
│ • ONU: Llamado a respetar DDHH tras detención │
│ • UE: Preocupación por situación humanitaria  │
│                                                │
└────────────────────────────────────────────────┘
```

---

## 10. ALGORITMOS DE PROCESAMIENTO

### 10.1 Scoring de Items

**Fórmula:**

```python
def calculate_item_score(item):
    """
    Calcula score combinado de relevancia para un item.
    
    Score range: 0.0 - 1.0
    """
    
    # 1. Editorial Score (40%)
    editorial_score = get_editorial_score(item)
    
    # 2. Engagement Score (30%)
    engagement_score = get_engagement_score(item)
    
    # 3. Recency Score (20%)
    recency_score = get_recency_score(item)
    
    # 4. Source Tier Score (10%)
    source_tier_score = get_source_tier_score(item)
    
    # Weighted combination
    total_score = (
        0.4 * editorial_score +
        0.3 * engagement_score +
        0.2 * recency_score +
        0.1 * source_tier_score
    )
    
    return round(total_score, 3)


def get_editorial_score(item):
    """
    Score basado en criterio editorial.
    
    Factores:
    - Medio independiente top: alto
    - Cobertura única vs. duplicada: alto
    - Profundidad vs. superficial: medio
    """
    
    base_score = 0.5
    
    # Bonus por tier de fuente
    tier_bonus = {
        'independiente': 0.3,
        'diaspora': 0.25,
        'internacional': 0.15,
        'estatal': 0.0  # Filtrado en otro layer
    }
    
    score = base_score + tier_bonus.get(item['source']['tier'], 0)
    
    # Penalty por contenido muy corto (< 100 palabras)
    if item.get('word_count', 200) < 100:
        score *= 0.7
    
    return min(score, 1.0)


def get_engagement_score(item):
    """
    Score basado en métricas de engagement.
    
    Solo aplica a videos (view_count).
    Para artículos, retorna score neutro.
    """
    
    if item['type'] != 'video':
        return 0.5  # Neutral para artículos
    
    views = item['metadata'].get('view_count', 0)
    
    # Logarithmic scaling para evitar que views dominen
    if views == 0:
        return 0.1
    
    # Benchmarks basados en audiencia cubana
    # 1K views = bajo
    # 10K views = medio
    # 50K+ views = alto
    
    import math
    score = math.log10(views + 1) / 5  # log10(50000) ≈ 4.7
    
    return min(score, 1.0)


def get_recency_score(item):
    """
    Score basado en qué tan reciente es el contenido.
    
    Decay exponencial:
    - < 6h: 1.0
    - < 12h: 0.8
    - < 24h: 0.5
    - > 24h: 0.2
    """
    
    from datetime import datetime, timezone
    
    now = datetime.now(timezone.utc)
    published = datetime.fromisoformat(item['content']['published_date'])
    
    hours_ago = (now - published).total_seconds() / 3600
    
    if hours_ago < 6:
        return 1.0
    elif hours_ago < 12:
        return 0.8
    elif hours_ago < 24:
        return 0.5
    else:
        return 0.2


def get_source_tier_score(item):
    """
    Score basado en tier configurado de la fuente.
    
    Mapping directo desde config.yaml
    """
    
    tier_scores = {
        'independiente': 1.0,
        'diaspora': 0.8,
        'internacional': 0.6,
        'estatal': 0.0  # Filtrado
    }
    
    return tier_scores.get(item['source']['tier'], 0.5)
```

### 10.2 Topic Clustering (LLM-based)

**Estrategia:** LLM decide si un nuevo item pertenece a un tema existente o crea uno nuevo.

**Algoritmo:**

```python
def assign_item_to_topic(item, existing_topics, llm_client):
    """
    Asigna un item a un tema existente o crea uno nuevo.
    
    Args:
        item: Item enriquecido con summary e insight
        existing_topics: Lista de temas del día actual
        llm_client: Cliente de Claude API
    
    Returns:
        topic_id: ID del tema asignado (existente o nuevo)
    """
    
    # Si no hay temas del día, crear el primero
    if not existing_topics:
        new_topic = create_new_topic(item, llm_client)
        return new_topic['id']
    
    # Preparar contexto para LLM
    prompt = build_clustering_prompt(item, existing_topics)
    
    # Llamar a Claude para decisión
    response = llm_client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=500,
        temperature=0.3,  # Baja para consistencia
        messages=[{"role": "user", "content": prompt}]
    )
    
    decision = parse_clustering_response(response.content)
    
    if decision['action'] == 'assign':
        # Asignar a tema existente
        topic_id = decision['topic_id']
        add_item_to_topic(topic_id, item)
        return topic_id
    
    else:  # decision['action'] == 'create'
        # Crear nuevo tema
        new_topic = create_new_topic(item, llm_client)
        return new_topic['id']


def build_clustering_prompt(item, existing_topics):
    """
    Construye prompt para decisión de clustering.
    """
    
    topics_description = "\n\n".join([
        f"TEMA {i+1}: {t['name']}\n"
        f"Síntesis: {t['synthesis']['narrative'][:200]}...\n"
        f"Items: {len(t['items']['featured']) + len(t['items']['additional'])}"
        for i, t in enumerate(existing_topics)
    ])
    
    prompt = f"""<sistema>
Eres un editor asignando noticias a temas del día.

Tu tarea: decidir si este nuevo item pertenece a un tema existente o necesita tema nuevo.

Criterios:
- ASIGNAR si el item trata sobre el mismo evento/situación que un tema existente
- CREAR tema nuevo si es un evento/situación diferente
- Temas deben ser coherentes narrativamente, no solo por keywords
</sistema>

<temas_existentes_hoy>
{topics_description}
</temas_existentes_hoy>

<nuevo_item>
Título: {item['content']['title']}
Fuente: {item['source']['name']} ({item['source']['tier']})
Resumen: {item['enrichment']['summary']}
Insight: {item['enrichment']['insight']}
</nuevo_item>

<tarea>
Responde en formato JSON:

Si debe asignarse a tema existente:
{{
  "action": "assign",
  "topic_id": "topic_20260412_XXX",
  "reason": "Explica brevemente por qué pertenece a ese tema"
}}

Si necesita tema nuevo:
{{
  "action": "create",
  "suggested_topic_name": "Nombre sugerido para nuevo tema",
  "reason": "Explica brevemente por qué necesita tema propio"
}}
</tarea>"""
    
    return prompt


def parse_clustering_response(response_text):
    """
    Parsea respuesta JSON de Claude.
    """
    import json
    import re
    
    # Extraer JSON (puede venir con texto adicional)
    json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
    if json_match:
        return json.loads(json_match.group())
    else:
        # Fallback: crear tema nuevo si hay error de parsing
        return {"action": "create", "suggested_topic_name": "Tema sin clasificar"}


def create_new_topic(item, llm_client):
    """
    Crea un nuevo tema basado en el primer item.
    """
    
    # Generar nombre del tema
    topic_name = generate_topic_name(item, llm_client)
    
    # Crear estructura de tema
    topic_id = f"topic_{datetime.now().strftime('%Y%m%d')}_{generate_short_id()}"
    
    new_topic = {
        'id': topic_id,
        'name': topic_name,
        'created_at': datetime.now(timezone.utc).isoformat(),
        'synthesis': {
            'narrative': item['enrichment']['summary'],  # Placeholder inicial
            'key_points': []
        },
        'items': {
            'featured': [item['id']],
            'additional': [],
            'videos': [item['id']] if item['type'] == 'video' else [],
            'state_coverage': []
        },
        'coverage': {
            'total_items': 1,
            item['source']['tier']: 1
        },
        'scoring': {
            'importance_score': item['scoring']['total_score'],
            'coverage_breadth': 0.1,  # Solo 1 item por ahora
            'total_score': item['scoring']['total_score'] * 0.1
        }
    }
    
    return new_topic
```

### 10.3 Deduplicación de Contenido

**Problema:** Múltiples medios cubren el mismo evento (ej: cable de AP republicado).

**Estrategia:**

```python
def detect_duplicates(new_item, existing_items):
    """
    Detecta si un nuevo item es duplicado de items existentes.
    
    Criterios:
    1. Title similarity > 0.85
    2. O (same day + keyword overlap > 80%)
    
    Returns:
        duplicate_of: ID del item original (o None)
        similarity_score: Score de similitud
    """
    
    from difflib import SequenceMatcher
    
    for existing in existing_items:
        # 1. Comparar títulos
        title_similarity = SequenceMatcher(
            None,
            new_item['content']['title'].lower(),
            existing['content']['title'].lower()
        ).ratio()
        
        if title_similarity > 0.85:
            return {
                'is_duplicate': True,
                'duplicate_of': existing['id'],
                'similarity_score': title_similarity,
                'method': 'title_similarity'
            }
        
        # 2. Comparar keywords + fecha
        if is_same_day(new_item, existing):
            keyword_overlap = calculate_keyword_overlap(new_item, existing)
            
            if keyword_overlap > 0.80:
                return {
                    'is_duplicate': True,
                    'duplicate_of': existing['id'],
                    'similarity_score': keyword_overlap,
                    'method': 'keyword_overlap'
                }
    
    return {'is_duplicate': False}


def handle_duplicate(new_item, original_item):
    """
    Maneja un item detectado como duplicado.
    
    Estrategia:
    - Si mismo medio: conservar más reciente, descartar antiguo
    - Si medios diferentes: marcar como "también cubierto por"
    """
    
    if new_item['source']['name'] == original_item['source']['name']:
        # Mismo medio: conservar más reciente
        if is_newer(new_item, original_item):
            replace_item(original_item['id'], new_item)
            return 'replaced'
        else:
            discard_item(new_item)
            return 'discarded'
    
    else:
        # Medios diferentes: agregar a "additional_coverage"
        add_to_additional_coverage(original_item['id'], new_item)
        return 'added_as_additional_coverage'
```

### 10.4 Generación de Síntesis de Tema

**Trigger:** Cuando un tema alcanza 3+ items.

```python
def generate_topic_synthesis(topic, items, llm_client):
    """
    Genera síntesis narrativa de un tema con múltiples items.
    """
    
    # Preparar contexto de todos los items del tema
    items_context = prepare_items_context(items)
    
    # Llamar prompt de síntesis
    prompt = build_topic_synthesis_prompt(topic, items_context)
    
    response = llm_client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1000,
        temperature=0.3,
        messages=[{"role": "user", "content": prompt}]
    )
    
    # Actualizar tema con síntesis
    topic['synthesis']['narrative'] = response.content[0].text
    
    # Extraer key points
    topic['synthesis']['key_points'] = extract_key_points(response.content[0].text)
    
    return topic
```

---

## 11. CONFIGURACIÓN DEL SISTEMA

### 11.1 Estructura `config.yaml`

```yaml
# CUBA DIGEST - Configuración Principal
# Versión: 2.0

project:
  name: "Cuba Digest"
  version: "2.0"
  environment: "development"  # development | production

sources:
  youtube:
    enabled: true
    api_key_env: "YOUTUBE_API_KEY"
    channels:
      - id: "UCxxxxxxxxxxx"
        name: "Juan Manuel Cao"
        tier: "diaspora"
        weight: 1.0
        enabled: true
      
      - id: "UCxxxxxxxxxxx"
        name: "Mario Pentón"
        tier: "diaspora"
        weight: 1.0
        enabled: true
      
      - id: "UCxxxxxxxxxxx"
        name: "Martí Noticias"
        tier: "independiente"
        weight: 1.0
        enabled: true
      
      - id: "UCxxxxxxxxxxx"
        name: "CiberCuba"
        tier: "independiente"
        weight: 0.9
        enabled: true
      
      # ... resto de canales
    
    extraction:
      max_videos_per_channel: 5
      lookback_hours: 24
      extract_captions: true
      captions_max_chars: 500
  
  rss:
    enabled: true
    feeds:
      - url: "https://cibercuba.com/rss"
        name: "CiberCuba"
        tier: "independiente"
        weight: 1.0
        enabled: true
      
      - url: "https://diariodecuba.com/rss"
        name: "Diario de Cuba"
        tier: "independiente"
        weight: 1.0
        enabled: true
      
      - url: "https://cubanet.org/feed/"
        name: "Cubanet"
        tier: "independiente"
        weight: 1.0
        enabled: true
      
      - url: "https://adncuba.com/rss"
        name: "ADN Cuba"
        tier: "independiente"
        weight: 0.9
        enabled: true
      
      - url: "https://www.14ymedio.com/feed/"
        name: "14ymedio"
        tier: "independiente"
        weight: 1.0
        enabled: true
      
      - url: "https://eltoque.com/rss"
        name: "El Toque"
        tier: "independiente"
        weight: 0.9
        enabled: true
      
      - url: "https://www.elnuevoherald.com/noticias/mundo/america-latina/cuba-es/rss"
        name: "El Nuevo Herald"
        tier: "diaspora"
        weight: 0.9
        enabled: true
      
      - url: "https://www.martinoticias.com/api/zr-oveqkit"
        name: "Martí Noticias"
        tier: "independiente"
        weight: 1.0
        enabled: true
      
      # Fuentes internacionales
      - url: "https://www.reuters.com/search/news?blob=cuba&sortBy=date"
        name: "Reuters"
        tier: "internacional"
        weight: 0.8
        enabled: true
      
      # Fuentes estatales (OFF por defecto en rendering)
      - url: "https://www.granma.cu/rss"
        name: "Granma"
        tier: "estatal"
        weight: 0.0
        enabled: false  # Colectar pero no mostrar por defecto
    
    extraction:
      max_items_per_feed: 10
      lookback_hours: 24

llm:
  provider: "anthropic"
  api_key_env: "ANTHROPIC_API_KEY"
  
  models:
    primary: "claude-3-haiku-20240307"
    fallback: "claude-3-haiku-20240307"
  
  defaults:
    temperature: 0.3
    max_tokens: 1000
  
  rate_limits:
    requests_per_minute: 50
    tokens_per_minute: 40000

processing:
  deduplication:
    enabled: true
    title_similarity_threshold: 0.85
    keyword_overlap_threshold: 0.80
  
  clustering:
    method: "llm_based"  # llm_based | embedding_based
    min_items_for_synthesis: 3
    similarity_threshold: 0.75  # No usado en LLM-based, pero disponible
  
  scoring:
    weights:
      editorial: 0.4
      engagement: 0.3
      recency: 0.2
      source_tier: 0.1
    
    tier_scores:
      independiente: 1.0
      diaspora: 0.8
      internacional: 0.6
      estatal: 0.0
  
  filtering:
    min_word_count: 50
    max_age_hours: 48
    exclude_tiers: []  # Tiers a excluir completamente

output:
  paths:
    data_dir: "./data"
    output_dir: "./output"
    templates_dir: "./templates"
  
  digest:
    filename: "digest_{date}.html"
    include_state_coverage: false  # Toggle default
  
  data_export:
    format: "json"  # json | yaml
    pretty_print: true

monitoring:
  logging:
    level: "INFO"  # DEBUG | INFO | WARNING | ERROR
    file: "./logs/cubadigest.log"
  
  metrics:
    enabled: true
    track_processing_time: true
    track_api_costs: true

schedule:
  generation_time: "09:00"  # UTC
  timezone: "America/Havana"
```

### 11.2 Estructura `prompts.yaml`

```yaml
# CUBA DIGEST - Prompt Templates
# Versión: 2.0

item_summary:
  system: |
    Eres un asistente editorial para Cuba Digest, un servicio de curación de noticias sobre Cuba.
    Tu rol: generar resúmenes objetivos, descriptivos y concisos.
    
    Principios:
    - Objetividad descriptiva (reportar hechos, no opinar)
    - Claridad y precisión
    - Español neutro
    - No copiar frases literales del original
    - Máximo 150 palabras
  
  user_template: |
    <contexto_fuente>
    Tipo: {content_type}
    Medio: {source_name}
    Clasificación: {source_tier}
    </contexto_fuente>
    
    <contenido_original>
    Título: {title}
    Descripción: {description}
    {captions_preview}
    </contenido_original>
    
    <tarea>
    Genera un resumen de 5-8 líneas que responda:
    - ¿Qué ocurrió/se reporta?
    - ¿Quién está involucrado?
    - ¿Cuándo y dónde?
    - ¿Por qué es relevante?
    
    Formato: párrafo corrido, sin bullets.
    </tarea>

item_insight:
  system: |
    Genera un insight editorial breve sobre este contenido.
    
    Principios:
    - Máximo 50 palabras
    - Indica qué aporta esta pieza al panorama
    - Mantén tono analítico, no sensacionalista
  
  user_template: |
    <item>
    Resumen: {summary}
    Fuente: {source_name} ({source_tier})
    Fecha: {date}
    </item>
    
    <contexto_dia>
    Otros items del día sobre temas relacionados:
    {related_items}
    </contexto_dia>
    
    <tarea>
    Responde brevemente:
    - ¿Qué ángulo único ofrece esta fuente?
    - ¿Qué agrega al entendimiento del tema?
    - ¿Por qué importa en el contexto del día?
    </tarea>

topic_synthesis:
  system: |
    Eres un editor senior sintetizando múltiples coberturas sobre un mismo tema.
    
    Principios:
    - Objetividad narrativa
    - Integrar perspectivas de múltiples fuentes
    - Señalar consensos y divergencias
    - Máximo 300 palabras
    - Español claro y periodístico
  
  user_template: |
    <items_agrupados>
    {items_list}
    </items_agrupados>
    
    <tarea>
    Genera una síntesis narrativa que:
    1. Explique qué está ocurriendo (el evento/situación central)
    2. Por qué varias fuentes lo están cubriendo
    3. Qué puntos hay en común entre las coberturas
    4. Qué divergencias o ángulos únicos aporta cada fuente
    5. Por qué esto importa en el contexto cubano actual
    
    Formato: 2-3 párrafos, tono analítico pero accesible.
    NO emitir opinión personal del sistema.
    Separar hechos de interpretaciones cuando las haya.
    </tarea>

topic_naming:
  system: |
    Genera un título descriptivo para un tema que agrupa múltiples noticias.
    
    Principios:
    - Máximo 8 palabras
    - Descriptivo, no sensacionalista
    - Que capture la esencia del tema
    - Sin verbos en infinitivo o gerundio
  
  user_template: |
    <sintesis_tema>
    {topic_synthesis}
    </sintesis_tema>
    
    <items_incluidos>
    {item_titles}
    </items_incluidos>
    
    <tarea>
    Genera un título que funcione como nombre del tema.
    
    Ejemplos de buenos títulos:
    - "Nuevas medidas económicas y reacciones"
    - "Brote de dengue en Santiago de Cuba"
    - "Apagones y crisis energética"
    - "Detención de activistas en La Habana"
    
    Evitar:
    - Títulos vagos: "Situación en Cuba"
    - Títulos sensacionalistas: "¡Crisis total!"
    - Títulos con gerundio: "Anunciando nuevas medidas"
    </tarea>

clustering_decision:
  system: |
    Eres un editor asignando noticias a temas del día.
    
    Tu tarea: decidir si este nuevo item pertenece a un tema existente o necesita tema nuevo.
    
    Criterios:
    - ASIGNAR si el item trata sobre el mismo evento/situación que un tema existente
    - CREAR tema nuevo si es un evento/situación diferente
    - Temas deben ser coherentes narrativamente, no solo por keywords
  
  user_template: |
    <temas_existentes_hoy>
    {existing_topics}
    </temas_existentes_hoy>
    
    <nuevo_item>
    Título: {item_title}
    Fuente: {source_name} ({source_tier})
    Resumen: {summary}
    Insight: {insight}
    </nuevo_item>
    
    <tarea>
    Responde en formato JSON:
    
    Si debe asignarse a tema existente:
    {
      "action": "assign",
      "topic_id": "topic_20260412_XXX",
      "reason": "Explica brevemente por qué pertenece a ese tema"
    }
    
    Si necesita tema nuevo:
    {
      "action": "create",
      "suggested_topic_name": "Nombre sugerido para nuevo tema",
      "reason": "Explica brevemente por qué necesita tema propio"
    }
    </tarea>
```

---

## 12. POLÍTICA DE CONTENIDO Y COPYRIGHT

### 12.1 Lo que SÍ se permite

✅ **Referenciar**
- Mencionar la fuente original
- Citar el medio y autor

✅ **Enlazar**
- Enlace directo a contenido original
- Botón "Leer original" siempre visible

✅ **Resumir**
- Síntesis en palabras propias
- Máximo 150 palabras por item

✅ **Sintetizar**
- Integrar múltiples fuentes
- Crear narrativa nueva

✅ **Generar insights propios**
- Análisis editorial
- Contextualización

### 12.2 Lo que NO se permite

❌ **Copiar artículos completos**
- Nunca reproducir texto íntegro
- Nunca copiar > 3 oraciones consecutivas

❌ **Transcribir videos completos**
- No usar transcripts como output principal
- Captions solo como contexto interno

❌ **Redistribuir contenido protegido**
- No replicar imágenes
- No descargar y rehosting videos

❌ **Reemplazar la fuente original**
- El producto incentiva ir al original
- No competir con medios fuente

### 12.3 Principio Fundamental

**El digest es una GUÍA hacia contenido original, no un SUSTITUTO.**

---

## 13. ARQUITECTURA TÉCNICA

### 13.1 Tipo de Sistema

**MVP:** Sistema local/personal con output estático compartible

**No requiere:**
- Base de datos persistente
- Autenticación de usuarios
- Panel de administración
- Analytics complejas
- Infraestructura cloud

### 13.2 Stack Técnico

#### Lenguaje Base
**Python 3.11+**

#### Librerías Core

```txt
# requirements.txt

# RSS Processing
feedparser==6.0.10

# YouTube
yt-dlp==2023.11.16
google-api-python-client==2.108.0

# LLM
anthropic==0.8.1

# HTML Templating
jinja2==3.1.2

# Data
pyyaml==6.0.1
python-dateutil==2.8.2

# Utilities
requests==2.31.0
beautifulsoup4==4.12.2
```

#### Estructura de Directorios

```
cuba-digest/
├── config/
│   ├── config.yaml
│   ├── prompts.yaml
│   └── sources.yaml
│
├── src/
│   ├── collectors/
│   │   ├── __init__.py
│   │   ├── youtube_collector.py
│   │   └── rss_collector.py
│   │
│   ├── processors/
│   │   ├── __init__.py
│   │   ├── enricher.py
│   │   ├── clusterer.py
│   │   ├── deduplicator.py
│   │   └── scorer.py
│   │
│   ├── renderers/
│   │   ├── __init__.py
│   │   └── html_renderer.py
│   │
│   └── utils/
│       ├── __init__.py
│       ├── llm_client.py
│       └── helpers.py
│
├── templates/
│   ├── landing.html
│   ├── digest.html
│   └── partials/
│       ├── header.html
│       ├── topic_card.html
│       └── item_card.html
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── cache/
│
├── output/
│   ├── digest_20260412.html
│   └── digest_20260413.html
│
├── logs/
│   └── cubadigest.log
│
├── tests/
│   ├── test_collectors.py
│   ├── test_processors.py
│   └── test_renderers.py
│
├── main.py
├── requirements.txt
├── README.md
└── .env.example
```

### 13.3 Pipeline de Ejecución

```python
# main.py - Simplified flow

def main():
    """
    Pipeline principal de generación de digest.
    """
    
    # 1. LOAD CONFIG
    config = load_config('config/config.yaml')
    prompts = load_prompts('config/prompts.yaml')
    
    # 2. COLLECT
    print("📥 Collecting sources...")
    youtube_items = collect_youtube(config['sources']['youtube'])
    rss_items = collect_rss(config['sources']['rss'])
    
    all_items = youtube_items + rss_items
    print(f"✅ Collected {len(all_items)} items")
    
    # 3. FILTER
    print("🔍 Filtering...")
    filtered_items = filter_items(all_items, config['processing']['filtering'])
    print(f"✅ {len(filtered_items)} items after filtering")
    
    # 4. DEDUPLICATE
    print("🔄 Deduplicating...")
    unique_items = deduplicate(filtered_items, config['processing']['deduplication'])
    print(f"✅ {len(unique_items)} unique items")
    
    # 5. ENRICH
    print("✨ Enriching with AI...")
    enriched_items = enrich_items(unique_items, prompts, config['llm'])
    print(f"✅ Enriched {len(enriched_items)} items")
    
    # 6. SCORE
    print("📊 Scoring...")
    scored_items = score_items(enriched_items, config['processing']['scoring'])
    
    # 7. CLUSTER
    print("🗂️  Clustering into topics...")
    topics = cluster_into_topics(scored_items, prompts, config['llm'])
    print(f"✅ Created {len(topics)} topics")
    
    # 8. SYNTHESIZE TOPICS
    print("📝 Generating topic syntheses...")
    synthesized_topics = synthesize_topics(topics, scored_items, prompts, config['llm'])
    
    # 9. RANK
    print("🏆 Ranking...")
    ranked_topics = rank_topics(synthesized_topics)
    ranked_items = rank_items(scored_items)
    
    # 10. RENDER HTML
    print("🎨 Rendering HTML...")
    digest_html = render_digest(
        topics=ranked_topics,
        items=ranked_items,
        config=config,
        date=datetime.now()
    )
    
    # 11. SAVE OUTPUT
    output_path = save_digest(digest_html, config['output'])
    print(f"✅ Digest saved to: {output_path}")
    
    # 12. OPEN IN BROWSER (optional)
    webbrowser.open(f'file://{os.path.abspath(output_path)}')

if __name__ == "__main__":
    main()
```

### 13.4 Datos Intermedios

**Formato:** JSON

**Ejemplo:**

```json
// data/processed/items_20260412.json
{
  "date": "2026-04-12",
  "items": [...],
  "topics": [...],
  "metadata": {
    "total_items_collected": 87,
    "items_after_filtering": 65,
    "unique_items": 52,
    "topics_created": 8,
    "processing_time_seconds": 45.2,
    "api_tokens_used": 38500
  }
}
```

---

## 14. ESTRATEGIA DE TESTING Y VALIDACIÓN

### 14.1 Pre-Share Checklist

**Antes de compartir un digest con testers, validar:**

#### ✅ Calidad de Contenido

- [ ] Al menos 5 temas identificados correctamente
- [ ] Ningún tema con < 2 fuentes (salvo breaking news)
- [ ] Resúmenes en español correcto (sin errores graves)
- [ ] Sin duplicados obvios (mismo contenido repetido)
- [ ] Síntesis de temas coherentes y útiles
- [ ] Insights agregan valor (no son genéricos)

#### ✅ Calidad Técnica

- [ ] Todos los enlaces funcionan (prueba manual de 10 aleatorios)
- [ ] HTML renderiza correctamente en desktop
- [ ] HTML renderiza correctamente en mobile
- [ ] Toggle "Cobertura estatal" funciona
- [ ] Tabs navegables sin errores
- [ ] Imágenes/thumbnails cargan (si se incluyen)

#### ✅ Posicionamiento Editorial

- [ ] Cobertura estatal separada (no mezclada en core)
- [ ] Fuentes clasificadas correctamente
- [ ] Ninguna síntesis con sesgo político obvio
- [ ] Nota contextual visible en sección estatal
- [ ] Medios independientes priorizados en temas

#### ✅ Experiencia de Usuario

- [ ] Core del día es claro y útil
- [ ] Temas tienen nombres descriptivos
- [ ] Navegación es intuitiva
- [ ] Tiempo de lectura razonable (~15-20 min)
- [ ] Landing explica el producto correctamente

### 14.2 Criterios de Aceptación

**Para considerar el digest "listo para compartir":**

| Criterio | Umbral Mínimo | Ideal |
|----------|---------------|-------|
| Temas identificados | 5 | 8-10 |
| Items únicos procesados | 30 | 50+ |
| Cobertura por tema | 2+ fuentes | 4+ fuentes |
| Calidad de resúmenes | 80% útiles | 95% útiles |
| Links rotos | 0% | 0% |
| Errores de español | < 2 por digest | 0 |
| Duplicados | < 5% | 0% |

### 14.3 Proceso de Validación Manual

**Día 1 - Validación Interna**

1. **Generación:** Ejecutar pipeline completo
2. **Revisión de Temas:**
   - Leer cada tema
   - Verificar coherencia narrativa
   - Confirmar que síntesis agrega valor
3. **Revisión de Clasificación:**
   - Verificar que fuentes estatales estén separadas
   - Confirmar que tiers son correctos
4. **Prueba de UX:**
   - Navegar cada tab
   - Verificar toggle estatal
   - Probar en móvil
5. **Decisión:** ¿Listo para compartir?

**Día 2-3 - Testing con 3-5 personas cercanas**

6. **Compartir digest**
7. **Recoger feedback:**
   - ¿Fue útil?
   - ¿Cuánto tiempo tomó leer?
   - ¿Qué faltó?
   - ¿Qué sobró?
8. **Iterar:**
   - Ajustar prompts
   - Refinar clustering
   - Mejorar UX

**Día 4-7 - Expansión a 10-15 testers**

9. **Compartir con grupo ampliado**
10. **Validar hipótesis:**
    - ¿Reduce ruido?
    - ¿Genera confianza?
    - ¿Vista por temas es útil?
    - ¿Separación estatal es valiosa?
    - ¿Se usaría diariamente?

### 14.4 Métricas de Testing

**Recoger manualmente (encuesta simple):**

```yaml
Encuesta Post-Lectura:

1. ¿Cuánto tiempo te tomó consumir el digest?
   - < 10 min
   - 10-20 min
   - 20-30 min
   - > 30 min

2. ¿Te sentiste bien informado después de leerlo?
   - Sí, completamente
   - Mayormente sí
   - Parcialmente
   - No

3. ¿Qué tab usaste más?
   - Temas
   - Medios
   - Videos
   - Trending
   - Cuba Global

4. ¿Activaste la cobertura estatal?
   - Sí
   - No

5. ¿Volverías a usar esto mañana?
   - Definitivamente sí
   - Probablemente sí
   - Quizás
   - No

6. ¿Qué mejorarías?
   [Texto libre]
```

---

## 15. MVP SHAREABLE

### 15.1 Objetivo

Compartir con **10-15 amigos/familia** para validar:

- ✅ Si reduce ruido
- ✅ Si genera confianza
- ✅ Si la vista por temas es útil
- ✅ Si la separación de cobertura estatal se percibe como valiosa
- ✅ Si el producto se usaría de forma diaria o semanal

### 15.2 Componentes del MVP

**1. Landing Simple**
- Explicación del producto
- Propuesta de valor
- CTA: "Ver Digest de Hoy"

**2. Digest HTML**
- 5 tabs funcionales
- Toggle cobertura estatal
- Responsive mobile

**3. Mecanismo de Feedback**
- Link a formulario Google Forms
- O WhatsApp para feedback rápido

### 15.3 Método de Distribución

**Opción A:** Archivo HTML enviado por email/WhatsApp
- Pros: Sin infraestructura
- Cons: Difícil de actualizar

**Opción B:** GitHub Pages (estático)
- Pros: URL fija, fácil actualizar
- Cons: Requiere setup mínimo

**Recomendación:** Opción B (GitHub Pages)

```bash
# Setup de GitHub Pages
1. Crear repo: cubadigest-mvp
2. Subir landing.html y digest.html a /docs
3. Activar GitHub Pages desde /docs
4. Compartir URL: https://{username}.github.io/cubadigest-mvp
```

### 15.4 Timeline MVP

```
Semana 1: Desarrollo
- Día 1-2: Collectors + estructura
- Día 3-4: Enrichment + clustering
- Día 5-6: HTML rendering
- Día 7: Testing interno

Semana 2: Testing
- Día 8: Validación interna
- Día 9-10: Testing con 3-5 cercanos
- Día 11-14: Expansión a 10-15 testers

Semana 3: Iteración
- Día 15-17: Incorporar feedback
- Día 18-19: Refinamiento
- Día 20-21: Decisión: ¿continuar?
```

---

## 16. MÉTRICAS DE ÉXITO

### 16.1 Métricas Iniciales (Semanas 1-3)

**Utilidad Percibida**
- Pregunta: "¿Te sentiste bien informado?"
- Target: 80%+ responden "Sí" o "Mayormente sí"

**Claridad**
- Pregunta: "¿Fue fácil navegar y entender el digest?"
- Target: 90%+ responden "Sí"

**Confianza**
- Pregunta: "¿Confías en la información presentada?"
- Target: 85%+ responden "Sí"

**Intención de Uso**
- Pregunta: "¿Volverías a usar esto mañana?"
- Target: 70%+ responden "Definitivamente sí" o "Probablemente sí"

**Tiempo de Consumo**
- Target: 80%+ completan en < 20 minutos

### 16.2 Métricas Futuras (Post-MVP)

**Recurrencia Semanal**
- ¿Cuántos usuarios regresan 3+ veces/semana?
- Target: 60%+ usuarios activos

**Tabs Más Usadas**
- Distribución de navegación
- Hipótesis: "Temas" será el más usado (60%+)

**Temas Más Leídos**
- Qué temas generan más engagement
- Insights para priorización editorial

**Fuentes Más Consultadas**
- Qué medios generan más clicks a original
- Validar peso de fuentes

**Feedback Cualitativo**
- Comentarios sobre qué falta
- Sugerencias de mejora

---

## 17. RIESGOS

### 17.1 Riesgos Técnicos

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| **Feeds inconsistentes** | Alta | Medio | Validación en collectors + logs detallados |
| **APIs de YouTube cambian** | Media | Alto | Usar yt-dlp (más estable que API directa) |
| **LLM genera contenido sesgado** | Media | Alto | Temperature baja + prompts con guardrails |
| **Clustering agrupa mal** | Media | Medio | Validación manual + iteración de prompts |

### 17.2 Riesgos de Producto

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| **Saturación visual** | Media | Medio | Límite de featured items por tema |
| **Bajo valor percibido** | Media | Alto | Enfoque en síntesis, no solo resumen |
| **Rechazo por cobertura estatal** | Baja | Medio | Separación clara + toggle OFF default |

### 17.3 Riesgos Legales

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| **Copyright infringement** | Baja | Alto | Nunca copiar > 150 palabras, siempre enlazar |
| **Reclamo de medio fuente** | Baja | Medio | Política clara: solo síntesis, no redistribución |

### 17.4 Riesgos Operacionales

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| **Costos de API escalan** | Media | Bajo | Monitoreo de costos + Haiku (económico) |
| **Mantenimiento insostenible** | Media | Alto | Automatización máxima + alertas |
| **Fuente clave desaparece** | Baja | Medio | Diversidad de fuentes |

---

## 18. ROADMAP DE IMPLEMENTACIÓN

### 18.1 Fase 1 — Foundation (Semana 1)

**Objetivo:** Pipeline básico funcionando con datos reales.

**Tasks:**

**Día 1-2: Setup + Collectors**
- [ ] Crear estructura de proyecto
- [ ] Setup `config.yaml` con fuentes reales
- [ ] Implementar `youtube_collector.py`
  - Extraer metadata
  - Extraer primeros 500 chars de captions
- [ ] Implementar `rss_collector.py`
  - Parsear feeds
  - Normalizar estructura
- [ ] Test: Colectar 10 items reales de cada tipo

**Día 3-4: Processing Básico**
- [ ] Implementar `filter.py`
  - Filtrar por edad
  - Filtrar por longitud mínima
- [ ] Implementar `deduplicator.py`
  - Title similarity
  - Keyword overlap
- [ ] Implementar `scorer.py`
  - Fórmula de scoring completa
- [ ] Test: Procesar 50 items reales

**Día 5-6: Enrichment + Clustering**
- [ ] Implementar `llm_client.py`
  - Wrapper de Anthropic API
  - Rate limiting
  - Error handling
- [ ] Implementar `enricher.py`
  - Summary generation
  - Insight generation
- [ ] Implementar `clusterer.py`
  - LLM-based clustering
  - Topic synthesis
  - Topic naming
- [ ] Test: Enriquecer y agrupar 30 items

**Día 7: HTML Rendering V1**
- [ ] Crear template `digest.html`
  - Header + toggle
  - Tab: Temas (solo este tab funcional)
- [ ] Implementar `html_renderer.py`
  - Jinja2 templating
  - Data binding
- [ ] Test: Generar digest.html completo
- [ ] **Milestone:** Primer digest HTML funcional

**Entregable Fase 1:**
- ✅ Digest HTML con tab "Temas" funcional
- ✅ Datos reales de fuentes
- ✅ Enriquecimiento con IA

### 18.2 Fase 2 — Completar Tabs (Semana 2)

**Objetivo:** Todas las vistas funcionando.

**Día 8-9: Tabs Medios + Videos**
- [ ] Implementar tab "Medios"
  - Agrupación por fuente
  - Orden cronológico
- [ ] Implementar tab "Videos"
  - Filtrado solo YouTube
  - Ranking por engagement

**Día 10-11: Tabs Trending + Cuba Global**
- [ ] Implementar tab "Trending"
  - Ordenar por views + engagement
- [ ] Implementar tab "Cuba Global"
  - Filtrar tier "internacional"
  - Sección especial

**Día 12: Cobertura Estatal**
- [ ] Implementar toggle funcional
  - JavaScript para show/hide
  - Persistencia en sessionStorage
- [ ] Agregar nota contextual
- [ ] Test: Validar que OFF es default

**Día 13: Landing Page**
- [ ] Crear `landing.html`
  - Explicación del producto
  - Propuesta de valor
  - CTA al digest
- [ ] Test: Navegación landing → digest

**Día 14: Polish + Mobile**
- [ ] Responsive design (mobile-first)
- [ ] Mejorar CSS/estética
- [ ] **Milestone:** MVP completo técnicamente

**Entregable Fase 2:**
- ✅ 5 tabs funcionales
- ✅ Toggle cobertura estatal
- ✅ Landing page
- ✅ Responsive mobile

### 18.3 Fase 3 — Testing Interno (Días 15-17)

**Objetivo:** Validar calidad antes de compartir.

**Día 15: Validación Profunda**
- [ ] Generar digest de día real
- [ ] Ejecutar checklist de validación
- [ ] Revisar cada tema manualmente
- [ ] Probar en 3 dispositivos

**Día 16: Correcciones**
- [ ] Ajustar prompts según hallazgos
- [ ] Corregir bugs detectados
- [ ] Refinar UX según problemas

**Día 17: Segunda Validación**
- [ ] Generar nuevo digest
- [ ] Re-validar checklist
- [ ] **Decisión GO/NO-GO para sharing**

**Entregable Fase 3:**
- ✅ Digest validado internamente
- ✅ Lista de issues conocidos (si los hay)
- ✅ Plan de mitigación

### 18.4 Fase 4 — MVP Shareable (Días 18-21)

**Objetivo:** Compartir con 10-15 testers y recoger feedback.

**Día 18: Setup Sharing**
- [ ] Subir a GitHub Pages
- [ ] Crear formulario de feedback
- [ ] Redactar email de invitación

**Día 19: Primera Ronda (3-5 personas)**
- [ ] Enviar invitaciones
- [ ] Recoger feedback inicial (24-48h)

**Día 20-21: Segunda Ronda (10-15 personas)**
- [ ] Incorporar feedback crítico
- [ ] Generar nuevo digest
- [ ] Expandir a grupo completo
- [ ] Recoger feedback ampliado

**Entregable Fase 4:**
- ✅ 10-15 personas testeando
- ✅ Feedback estructurado
- ✅ Insights clave sobre producto

### 18.5 Fase 5 — Iteración (Semana 4+)

**Basado en feedback, iterar:**

**Mejoras Probables:**
- Ajustar prompts para mejor síntesis
- Refinar clustering (menos/más temas)
- Optimizar UX mobile
- Agregar nuevas fuentes
- Mejorar estética

**Decisión Post-Iteración:**
- ¿Continuar desarrollando?
- ¿Automatizar generación diaria?
- ¿Escalar a más usuarios?
- ¿Monetización futura?

---

## 19. ARTIFACTS DE IMPLEMENTACIÓN

### 19.1 Checklist de Setup Inicial

```bash
# 1. Crear directorio de proyecto
mkdir cuba-digest
cd cuba-digest

# 2. Crear estructura
mkdir -p src/{collectors,processors,renderers,utils}
mkdir -p config templates data/{raw,processed,cache} output logs tests

# 3. Setup virtual environment
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Copiar config templates
cp config/config.yaml.example config/config.yaml
cp .env.example .env

# 6. Configurar API keys
# Editar .env:
# ANTHROPIC_API_KEY=tu_key_aqui
# YOUTUBE_API_KEY=tu_key_aqui

# 7. Validar setup
python -c "import anthropic; print('✅ Anthropic OK')"
python -c "import feedparser; print('✅ Feedparser OK')"

# 8. Test run
python main.py --dry-run
```

### 19.2 Ejemplo de .env

```bash
# CUBA DIGEST - Environment Variables

# Anthropic API
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# YouTube API (opcional si usas yt-dlp)
YOUTUBE_API_KEY=AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Environment
ENVIRONMENT=development  # development | production

# Logging
LOG_LEVEL=INFO  # DEBUG | INFO | WARNING | ERROR
```

### 19.3 Comandos Útiles

```bash
# Generar digest de hoy
python main.py

# Generar digest de fecha específica
python main.py --date 2026-04-12

# Modo dry-run (sin llamadas a API)
python main.py --dry-run

# Solo colectar (sin procesar)
python main.py --collect-only

# Solo renderizar (desde datos existentes)
python main.py --render-only

# Ver logs en tiempo real
tail -f logs/cubadigest.log

# Limpiar cache
rm -rf data/cache/*

# Tests
pytest tests/
```

---

## APÉNDICES

### A. Glosario

**Item:** Unidad atómica del sistema (un artículo o un video)

**Tema (Topic):** Agrupación narrativa de múltiples items relacionados

**Tier:** Clasificación editorial de fuente (independiente, diáspora, internacional, estatal)

**Score:** Puntaje de relevancia calculado algorítmicamente

**Clustering:** Proceso de agrupar items en temas

**Enrichment:** Proceso de agregar resúmenes, insights y metadata con IA

**Digest:** Output final HTML multi-vista

**Toggle:** Control para mostrar/ocultar cobertura estatal

**Core del Día:** Resumen principal de los temas más importantes

### B. Referencias

**Inspiración Editorial:**
- The Browser (thebrowser.com)
- Stratechery by Ben Thompson
- Not Boring by Packy McCormick

**Frameworks de Curación:**
- Maria Popova's Brain Pickings methodology
- Exploding Topics trend curation

**Tecnología:**
- Anthropic Claude API Docs
- yt-dlp documentation
- Jinja2 templating guide

### C. FAQ Técnicas

**Q: ¿Por qué Haiku y no Sonnet?**
A: Para MVP, Haiku es suficiente para síntesis objetiva y es 10x más económico. Podemos escalar a Sonnet si la calidad lo requiere.

**Q: ¿Por qué LLM-based clustering y no embeddings?**
A: Para MVP, LLM-based es más simple de implementar y debugear. Embeddings requieren vector DB y es over-engineering para 50 items/día.

**Q: ¿Por qué HTML estático y no webapp?**
A: Para MVP, HTML estático es suficiente y no requiere infraestructura. Podemos evolucionar a webapp si hay tracción.

**Q: ¿Cómo manejo rate limits de Claude?**
A: Haiku tiene límite de 50 req/min. Con 50 items/día, procesamos en ~5 minutos sin problemas. Agregamos retry con backoff exponencial.

**Q: ¿Qué pasa si una fuente cambia su RSS?**
A: Logs detectarán el error. Agregamos alertas básicas y validación manual semanal de fuentes.

---

## CONCLUSIÓN

Este PRD v2.0 proporciona **especificaciones técnicas completas** para implementar Cuba Digest con Claude Code.

**Gaps críticos resueltos:**
- ✅ Estrategia de IA y enriquecimiento definida
- ✅ Algoritmos de procesamiento especificados
- ✅ Topic clustering con LLM detallado
- ✅ Scoring y ranking con fórmulas exactas
- ✅ Configuración estructurada (YAML)
- ✅ Testing y validación con checklists
- ✅ Roadmap de implementación por fases

**Próximo paso:**
Comenzar Fase 1 con Claude Code — setup de proyecto y primer collector funcional.

---

**Versión:** 2.0  
**Estado:** ✅ Ready for Implementation  
**Última actualización:** 2026-04-12  
**Optimizado por:** ARCHIE v1.1 + Gigawatt v5.1 (prompts)
