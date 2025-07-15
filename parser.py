# parser.py
from rdflib import Graph, RDF, OWL, RDFS
import re

def clean_iri(iri):
    return iri.split("#")[-1] if "#" in iri else iri.split("/")[-1]

def describe_restriction(g, bnode):
    description = ""
    prop = g.value(bnode, OWL.onProperty)
    datatype = g.value(bnode, OWL.someValuesFrom)
    ondatatype = g.value(datatype, OWL.onDatatype)
    restrictions = list(g.objects(datatype, OWL.withRestrictions))

    readable_prop = clean_iri(prop)

    if restrictions:
        r = restrictions[0]
        for item in g.items(r):
            for p, o in g.predicate_objects(item):
                if "minInclusive" in p:
                    description += f"{readable_prop} ≥ {o} "
                elif "maxInclusive" in p:
                    description += f"{readable_prop} ≤ {o} "
    return description.strip()

def parse_ontology(filepath):
    g = Graph()
    g.parse(filepath, format="ttl")
    chunks = []

    for cls in g.subjects(RDF.type, OWL.Class):
        cls_name = clean_iri(cls)
        for eq in g.objects(cls, OWL.equivalentClass):
            if (eq, OWL.intersectionOf, None) in g:
                lines = [f"A lake is classified as **{cls_name}** if:"]
                collection = g.value(eq, OWL.intersectionOf)
                for item in g.items(collection):
                    if (item, RDF.type, OWL.Restriction) in g:
                        lines.append("- " + describe_restriction(g, item))
                    elif (item, RDF.type, OWL.Class) in g:
                        lines.append(f"- It is a {clean_iri(item)}")
                chunks.append("\n".join(lines))

    for subclass, _, superclass in g.triples((None, RDFS.subClassOf, None)):
        if (subclass, RDF.type, OWL.Class) in g and (superclass, RDF.type, OWL.Class) in g:
            chunks.append(f"{clean_iri(subclass)} is a subclass of {clean_iri(superclass)}.")

    for cls in g.subjects(RDF.type, OWL.Class):
        label = g.value(cls, RDFS.label)
        comment = g.value(cls, RDFS.comment)
        lines = [f"Class: {clean_iri(cls)}"]
        if label:
            lines.append(f"- Label: {label}")
        if comment:
            lines.append(f"- Comment: {comment}")
        if len(lines) > 1:
            chunks.append("\n".join(lines))

    for prop in g.subjects(RDF.type, OWL.ObjectProperty):
        domain = g.value(prop, RDFS.domain)
        range_ = g.value(prop, RDFS.range)
        chunks.append(
            f"Object Property: {clean_iri(prop)}\n- Domain: {clean_iri(domain) if domain else 'Unknown'}\n- Range: {clean_iri(range_) if range_ else 'Unknown'}"
        )

    for prop in g.subjects(RDF.type, OWL.DatatypeProperty):
        domain = g.value(prop, RDFS.domain)
        range_ = g.value(prop, RDFS.range)
        chunks.append(
            f"Data Property: {clean_iri(prop)}\n- Domain: {clean_iri(domain) if domain else 'Unknown'}\n- Range: {range_ if range_ else 'Unknown'}"
        )

    class_properties = {}
    for prop in g.subjects(RDF.type, (OWL.ObjectProperty, OWL.DatatypeProperty)):
        domain = g.value(prop, RDFS.domain)
        if domain:
            domain_name = clean_iri(domain)
            class_properties.setdefault(domain_name, []).append(clean_iri(prop))

    for cls, props in class_properties.items():
        chunks.append(f"{cls} has properties: {', '.join(props)}.")

    for indiv in g.subjects(RDF.type, None):
        if (indiv, RDF.type, OWL.Class) in g:
            continue
        indiv_name = clean_iri(indiv)
        indiv_type = g.value(indiv, RDF.type)
        if indiv_type:
            lines = [f"Individual: {indiv_name}"]
            lines.append(f"- Type: {clean_iri(indiv_type)}")
            for p, o in g.predicate_objects(indiv):
                if p == RDF.type:
                    continue
                prop_name = clean_iri(p)
                obj_val = clean_iri(o) if isinstance(o, str) else str(o)
                lines.append(f"- {prop_name}: {obj_val}")
            chunks.append("\n".join(lines))

    return chunks
