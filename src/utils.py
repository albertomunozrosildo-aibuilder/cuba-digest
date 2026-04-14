"""Shared utilities for Cuba Digest."""

import hashlib
import logging
import re
import yaml
from datetime import datetime, timezone
from pathlib import Path


def load_yaml(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def setup_logging(level: str = "INFO", log_file: str = None):
    handlers = [logging.StreamHandler()]
    if log_file:
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        handlers.append(logging.FileHandler(log_file, encoding="utf-8"))

    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
        handlers=handlers,
    )


def make_item_id(date_str: str, url: str) -> str:
    """Stable ID from date + URL."""
    slug = hashlib.md5(url.encode()).hexdigest()[:8]
    return f"item_{date_str}_{slug}"


def make_topic_id(date_str: str, name: str) -> str:
    slug = hashlib.md5(name.encode()).hexdigest()[:6]
    return f"topic_{date_str}_{slug}"


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def parse_date(value) -> datetime | None:
    """Parse various date formats into a timezone-aware datetime."""
    if value is None:
        return None
    if isinstance(value, datetime):
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value
    if isinstance(value, str):
        try:
            from dateutil import parser as dp
            dt = dp.parse(value)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except Exception:
            return None
    # time.struct_time from feedparser
    try:
        import calendar
        ts = calendar.timegm(value)
        return datetime.fromtimestamp(ts, tz=timezone.utc)
    except Exception:
        return None


def clean_html(text: str) -> str:
    """Strip HTML tags, emojis, and normalise whitespace."""
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", " ", text)
    # Use _strip_emoji to remove symbols while preserving Spanish accented letters
    text = _strip_emoji(text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _strip_emoji(text: str) -> str:
    """Remove emoji and symbol characters while preserving Spanish letters."""
    result = []
    for char in text:
        cp = ord(char)
        # Keep: basic Latin, Latin Extended (Spanish), common punctuation
        if cp < 0x2000:
            result.append(char)
        # Keep: general punctuation range that includes useful chars
        elif 0x2013 <= cp <= 0x2026:  # — … –
            result.append(char)
        # Drop: everything else (emojis, symbols, dingbats, etc.)
    return "".join(result)


# Boilerplate phrases that appear at the end of RSS snippets
_BOILERPLATE = re.compile(
    r"\s*(Leer más|Ver más|Read more|Continuar leyendo|La entrada .+ apareció primero"
    r"|The post .+ appeared first|\[\.\.\.\]|\[…\]|…$)",
    re.IGNORECASE,
)

# YouTube promo blocks: membership calls, social links, PayPal, etc.
# These appear at the top or bottom of video descriptions.
_YT_PROMO_BLOCK = re.compile(
    r"(QUIERES APOYAR|MIEMBRO DE LA PEÑA|Hazte miembro|ÚNETE AL CANAL"
    r"|paypal|cashapp|zelle|venmo|patreon|subscribestar"
    r"|síguenos en|follow us|instagram:|twitter:|facebook:|telegram:"
    r"|www\.youtube\.com/channel/[^\s]+/join"
    r"|suscríbete|subscribe|dale like|comparte este video"
    r"|canal de youtube|nuestro canal)",
    re.IGNORECASE,
)


def _strip_yt_promo(text: str) -> str:
    """
    Remove YouTube promotional paragraphs from a video description.
    Splits by newline and discards any paragraph that contains promo signals.
    Returns only the clean informational paragraphs.
    """
    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
    clean = []
    for p in paragraphs:
        if _YT_PROMO_BLOCK.search(p):
            continue
        # Drop paragraphs that are mostly URLs or emojis (no real words)
        words = re.findall(r"[a-záéíóúüñA-Z]{3,}", p)
        if len(words) < 3:
            continue
        clean.append(p)
    return " ".join(clean)


def first_sentences(text: str, n: int = 3, max_chars: int = 250) -> str:
    """Return first n sentences from plain text, capped at max_chars."""
    if not text:
        return ""
    text = clean_html(text)
    # Strip YouTube promo blocks before sentence extraction
    text = _strip_yt_promo(text)
    # Strip RSS boilerplate
    text = _BOILERPLATE.sub("", text).strip()
    if not text:
        return ""
    # Split on sentence-ending punctuation
    sentences = re.split(r"(?<=[.!?])\s+", text)
    result = " ".join(sentences[:n]).strip()
    if len(result) > max_chars:
        result = result[:max_chars].rsplit(" ", 1)[0] + "…"
    return result


# ── Keyword extraction ────────────────────────────────────────────────────────

# Words too generic to use as clustering signals
_STOPWORDS = {
    # Spanish function words
    "para", "como", "pero", "este", "esta", "esto", "estos", "estas",
    "desde", "hasta", "cuando", "donde", "sobre", "entre", "durante",
    "ante", "bajo", "cada", "cual", "cuyo", "ella", "ellos", "ello",
    "mismo", "otra", "otro", "pues", "solo", "toda", "todo", "todos",
    "según", "dice", "dijo", "también", "después", "aunque", "porque",
    "tiene", "hace", "está", "están", "será", "eran", "sería",
    # English function words
    "also", "that", "this", "with", "from", "have", "been", "will",
    "were", "their", "they", "what", "which", "more", "than", "after",
    "said", "says", "just", "could", "would", "should", "about",
    # Overly generic Cuba-context words that match EVERY article
    # and create false keyword overlaps in the clusterer
    "cuba", "cubano", "cubana", "cubanos", "cubanas",
    "habana", "habanas", "habanero", "habanera",
    "isla", "islas", "país", "pais", "nación",
    "gobierno", "régimen", "estado", "estados", "partido",
    "nuevo", "nueva", "nuevos", "nuevas",
    "muere", "muerte", "muerto", "muertos",
    "primera", "primero", "últimas", "último",
    "sido", "haber", "hacer",
    # Generic "states/countries" that appear in many articles
    "unidos", "unidas", "unido",
    # Generic news words
    "según", "informó", "señaló", "indicó", "aseguró", "explicó",
    "declaró", "afirmó", "noticia", "noticias", "nota", "artículo",
    "video", "foto", "imagen",
}


def extract_keywords(text: str) -> list[str]:
    """Extract discriminating keywords (non-stopword tokens ≥4 chars)."""
    text = clean_html(text).lower()
    tokens = re.findall(r"\b[a-záéíóúüña-z]{4,}\b", text)
    seen: set[str] = set()
    keywords: list[str] = []
    for tok in tokens:
        if tok not in _STOPWORDS and tok not in seen:
            seen.add(tok)
            keywords.append(tok)
    return keywords[:20]


# ── Topic category classification ─────────────────────────────────────────────

_CATEGORY_KEYWORDS: dict[str, list[str]] = {
    "política": [
        "díaz-canel", "diazcanal", "presidente", "asamblea", "congreso",
        "partido", "ministerio", "oposición", "disidente", "presos políticos",
        "represión", "dictadura", "totalitario", "elecciones",
    ],
    "economía": [
        "economía", "crisis económica", "inflación", "precios", "petróleo",
        "combustible", "alimentos", "escasez", "dólar", "divisas", "mipymes",
        "empresa", "inversión", "comercio", "desabastecimiento", "salario",
        "remesas", "apagón", "apagones", "electricidad", "energía",
    ],
    "derechos_humanos": [
        "preso", "presos", "prisionero", "arrestado", "detenido", "liberado",
        "activista", "manifestante", "protesta", "huelga", "torturas",
        "juicio", "condena", "sentencia", "acusado", "11julio",
        "feminicidio", "violencia", "represión",
    ],
    "migración": [
        "emigración", "migración", "migrante", "migrantes", "refugiado",
        "deportado", "deportación", "exilio", "exiliado", "balsero",
        "visa", "parole", "asilo", "frontera", "título 8", "cbp",
        "salida", "huida", "abandonan", "escapan", "éxodo",
    ],
    "sociedad": [
        "familia", "salud", "hospital", "médico", "educación",
        "transporte", "vivienda", "internet", "telecomunicaciones",
        "apagón", "agua", "racionamiento", "escuela", "universidad",
    ],
    "internacional": [
        "estados unidos", "eeuu", "trump", "biden", "sanciones", "embargo",
        "relaciones exteriores", "diplomático", "acuerdo", "tratado",
        "naciones unidas", "europa", "rusia", "china", "venezuela",
        "latinoamérica", "caribe",
    ],
    "cultura": [
        "música", "arte", "cultura", "cine", "película", "literatura",
        "escritor", "artista", "deportes", "béisbol", "fútbol", "atleta",
    ],
}


def classify_category(text: str) -> str:
    """Classify text into a Cuba-news topic category."""
    text_lower = (text or "").lower()
    scores: dict[str, int] = {}
    for cat, keywords in _CATEGORY_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text_lower)
        if score:
            scores[cat] = score
    if not scores:
        return "general"
    return max(scores, key=lambda k: scores[k])


_CATEGORY_LABELS_ES = {
    "política": "Política",
    "economía": "Economía",
    "migración": "Migración",
    "derechos_humanos": "Derechos Humanos",
    "sociedad": "Sociedad",
    "internacional": "Internacional",
    "cultura": "Cultura",
    "general": "General",
}


def category_label_es(category: str) -> str:
    return _CATEGORY_LABELS_ES.get(category, category.title())
