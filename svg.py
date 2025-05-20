#!/usr/bin/env python3

from argparse import ArgumentParser
from pathlib import Path
from xml.etree import ElementTree as ET


def strip_ns(elem):
    """Recursively remove namespace prefixes like 'ns0:'"""
    for el in elem.iter():
        if "}" in el.tag:
            el.tag = el.tag.split("}", 1)[1]  # strip namespace


def clean_svg_content(svg_path):
    tree = ET.parse(svg_path)
    root = tree.getroot()

    viewBox = root.attrib.get("viewBox")
    if not viewBox:
        raise ValueError(f"{svg_path.name} is missing a viewBox attribute")

    # Extract inherited attributes from outer <svg>
    inherited_attrs = {}
    for attr in [
        "stroke",
        "fill",
        "color",
        "stroke-width",
        "stroke-linecap",
        "stroke-linejoin",
        "stroke-miterlimit",
    ]:
        if attr in root.attrib:
            inherited_attrs[attr] = root.attrib[attr]

    symbol = ET.Element(
        "symbol",
        {
            "id": svg_path.stem,
            "viewBox": viewBox,
        },
    )

    for child in list(root):
        # Copy inherited attributes if child doesn't override
        for attr, value in inherited_attrs.items():
            if child.tag.endswith("path") and attr not in child.attrib:
                child.set(attr, value)
        symbol.append(child)

    strip_ns(symbol)
    return symbol


def generate_sprite(icon_dir, path):
    symbols = []

    for file in Path(icon_dir).glob("*.svg"):
        symbol = clean_svg_content(file)
        symbols.append(symbol)

    svg = ET.Element(
        "svg",
        {
            "xmlns": "http://www.w3.org/2000/svg",
            "style": "display: none;",
        },
    )

    for sym in symbols:
        svg.append(sym)

    ET.indent(svg, space="  ")
    ET.ElementTree(svg).write(path, encoding="utf-8", xml_declaration=False)


if __name__ == "__main__":
    parser = ArgumentParser(description="Generate SVG sprite sheet.")
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        help="Input directory containing SVG files",
        required=True,
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Output file path",
        required=True,
    )
    args = parser.parse_args()

    generate_sprite(args.input, args.output)
