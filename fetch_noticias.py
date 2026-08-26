#!/usr/bin/env python3
"""
Descarga titulares de política española desde RSS públicos y actualiza noticias.json.
Pensado para ejecutarse a diario vía GitHub Actions. Solo usa la librería estándar
de Python, así que no requiere instalar dependencias.

Para añadir o quitar medios, edita la lista FUENTES.
"""
import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from html import unescape

FUENTES = [
    {"nombre": "elDiario.es", "url": "https://www.eldiario.es/rss/"},
    {"nombre": "El País (España)", "url": "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/espana/portada"},
    {"nombre": "20minutos", "url": "https://www.20minutos.es/rss/"},
    {"nombre": "Público", "url": "https://www.publico.es/rss/"},
]

# Palabras clave para quedarnos solo con noticias de política
PALABRAS_POLITICA = [
    "gobierno", "congreso", "senado", "ministr", "ministeri", "diputad",
    "presidente", "presidenta", "moncloa", "elecciones", "partido",
    "psoe", "pp ", "vox", "sumar", "podemos", "junts", "erc", "bildu",
    "corrupción", "corrupcion", "dimisión", "dimision", "moción",
    "mocion", "parlament", "constitucional", "fiscalía", "fiscalia",
    "comunidad autónoma", "ayuntamiento", "política", "politica",
]

# Palabras que elevan la urgencia de una noticia
PALABRAS_URGENTES = [
    "dimite", "dimisión", "dimision", "corrupción", "corrupcion",
    "imputad", "detenid", "moción de censura", "mocion de censura",
    "cesa", "escándalo", "escandalo", "investigación judicial",
]

MAX_NOTICIAS = 40
ARCHIVO = "noticias.json"


def limpiar_html(texto):
    if not texto:
        return ""
    texto = re.sub(r"<[^>]+>", "", texto)
    return unescape(texto).strip()


def es_de_politica(titulo, resumen):
    texto = f"{titulo} {resumen}".lower()
    return any(p in texto for p in PALABRAS_POLITICA)


def nivel_de(titulo, resumen):
    texto = f"{titulo} {resumen}".lower()
    if any(p in texto for p in PALABRAS_URGENTES):
        return "urgente"
    return "seguimiento"


def descargar(url):
    req = urllib.request.Request(url, headers={"User-Agent": "EnPieBot/1.0 (+proyecto ciudadano)"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read()


def parsear_rss(xml_bytes, fuente_nombre):
    items = []
    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError:
        return items

    for item in root.iter():
        tag = item.tag.split("}")[-1]  # ignora namespaces (Atom/MRSS)
        if tag not in ("item", "entry"):
            continue

        titulo = resumen = enlace = fecha = ""
        for child in item:
            ctag = child.tag.split("}")[-1]
            if ctag == "title":
                titulo = limpiar_html(child.text)
            elif ctag in ("description", "summary"):
                resumen = limpiar_html(child.text)[:220]
            elif ctag == "link":
                enlace = (child.text or child.get("href") or "").strip()
            elif ctag in ("pubDate", "published", "updated"):
                fecha = (child.text or "").strip()

        if titulo and enlace:
            items.append({
                "titulo": titulo,
                "resumen": resumen,
                "fuente": fuente_nombre,
                "enlace": enlace,
                "fecha_raw": fecha,
            })
    return items


def normalizar_fecha(fecha_raw):
    formatos = ["%a, %d %b %Y %H:%M:%S %z", "%a, %d %b %Y %H:%M:%S %Z", "%Y-%m-%dT%H:%M:%S%z"]
    for f in formatos:
        try:
            return datetime.strptime(fecha_raw, f).astimezone(timezone.utc).strftime("%Y-%m-%d")
        except (ValueError, TypeError):
            continue
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def main():
    try:
        with open(ARCHIVO, "r", encoding="utf-8") as f:
            existentes = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        existentes = []

    enlaces_existentes = {n.get("enlace") for n in existentes}
    nuevas = []

    for fuente in FUENTES:
        try:
            xml_bytes = descargar(fuente["url"])
        except Exception as e:
            print(f"Aviso: no se pudo leer {fuente['nombre']} ({e})")
            continue

        for item in parsear_rss(xml_bytes, fuente["nombre"]):
            if item["enlace"] in enlaces_existentes:
                continue
            if not es_de_politica(item["titulo"], item["resumen"]):
                continue
            nuevas.append({
                "titulo": item["titulo"],
                "resumen": item["resumen"],
                "fuente": item["fuente"],
                "enlace": item["enlace"],
                "fecha": normalizar_fecha(item["fecha_raw"]),
                "nivel": nivel_de(item["titulo"], item["resumen"]),
            })
            enlaces_existentes.add(item["enlace"])

    # quitamos la tarjeta de bienvenida de ejemplo en cuanto haya noticias reales
    existentes = [n for n in existentes if n.get("fuente") != "EN PIE"]

    todas = nuevas + existentes
    todas.sort(key=lambda n: n.get("fecha", ""), reverse=True)
    todas = todas[:MAX_NOTICIAS]

    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(todas, f, ensure_ascii=False, indent=2)

    print(f"Añadidas {len(nuevas)} noticias nuevas. Total en el archivo: {len(todas)}.")


if __name__ == "__main__":
    main()
