"""Check content shape and normalized source preservation; no RDF/OWL reasoning."""

import argparse
import json
from pathlib import Path


def _text(value):
    return isinstance(value, str) and bool(value.strip())


def _enum(value, options):
    return _text(value) and value in options


def _labels(term):
    if not isinstance(term.get("labels"), list):
        return set()
    return {
        (label.get("text"), label.get("language"), label.get("role"))
        for label in term.get("labels", [])
        if isinstance(label, dict)
        and all(_text(label.get(k)) for k in ("text", "language", "role"))
    }


def _edge(relation):
    return tuple(relation.get(key) for key in ("subject", "predicate", "object", "status"))


def validate(data, baseline=None):
    errors = []
    if not isinstance(data, dict):
        return ["content must be an object"]
    for key in ("title", "intro", "domain", "language", "scope_note"):
        if not _text(data.get(key)):
            errors.append(f"{key} must be nonempty text")
    if not _enum(data.get("coverage"), {"complete", "curated"}):
        errors.append("coverage must be complete or curated")
    lists = {}
    for key in ("sections", "terms", "external_terms", "relations", "sources"):
        value = data.get(key)
        if not isinstance(value, list) or any(not isinstance(x, dict) for x in value):
            errors.append(f"{key} must be an array of objects")
            lists[key] = []
        else:
            lists[key] = value
    if not lists["terms"] or not lists["sections"]:
        errors.append("content needs at least one term and section")
    indexed = {}
    for key in ("sections", "terms", "external_terms", "sources"):
        ids = [item.get("id") for item in lists[key]]
        if any(not _text(x) for x in ids):
            errors.append(f"{key} has a missing or invalid id")
        valid_ids = [x for x in ids if _text(x)]
        if len(set(valid_ids)) != len(valid_ids):
            errors.append(f"{key} has duplicate ids")
        indexed[key] = {item["id"]: item for item in lists[key] if _text(item.get("id"))}
    if set(indexed["terms"]) & set(indexed["external_terms"]):
        errors.append("an id cannot be both a term and an external endpoint")
    for section in lists["sections"]:
        for key in ("title", "intro"):
            if not _text(section.get(key)):
                errors.append(f"section {section.get('id')} needs {key}")
    for source in lists["sources"]:
        if not _text(source.get("title")) or not _text(source.get("locator")):
            errors.append(f"source {source.get('id')} needs title and locator")

    def check_sources(item, location):
        refs = item.get("source_ids")
        if not isinstance(refs, list) or any(not _text(x) for x in refs):
            errors.append(f"{location} source_ids must be an array of strings")
        elif any(x not in indexed["sources"] for x in refs):
            errors.append(f"{location} references an undefined source")

    for term in lists["terms"]:
        location = f"term {term.get('id')}"
        for key in ("label", "kind", "definition"):
            if not _text(term.get(key)):
                errors.append(f"{location} needs {key}")
        if not _text(term.get("section_id")) or term["section_id"] not in indexed["sections"]:
            errors.append(f"{location} has an undefined section")
        labels = term.get("labels")
        if (
            not isinstance(labels, list)
            or not labels
            or any(not isinstance(x, dict) for x in labels)
        ):
            errors.append(f"{location} needs labels")
        else:
            for label in labels:
                if (
                    not _text(label.get("text"))
                    or not _text(label.get("language"))
                    or not _enum(
                        label.get("role"), {"preferred", "alternate", "hidden", "generated"}
                    )
                ):
                    errors.append(f"{location} has an invalid label")
            if not any(
                x.get("text") == term.get("label") and x.get("role") != "hidden" for x in labels
            ):
                errors.append(f"{location} displayed label is absent or hidden")
        check_sources(term, location)
    endpoints = set(indexed["terms"]) | set(indexed["external_terms"])
    edges = set()
    for relation in lists["relations"]:
        if any(not _text(relation.get(key)) for key in ("subject", "predicate", "object")):
            errors.append("relation requires identifier-valued subject, predicate, object")
            continue
        if relation.get("subject") not in endpoints or relation.get("object") not in endpoints:
            errors.append("relation has an undefined endpoint")
        if not _enum(relation.get("status"), {"asserted", "inferred", "proposed"}):
            errors.append("relation status must be asserted, inferred, or proposed")
            continue
        check_sources(relation, "relation")
        edge = _edge(relation)
        if edge in edges:
            errors.append("duplicate relation")
        edges.add(edge)
    if baseline is not None:
        if (
            not isinstance(baseline, dict)
            or not _enum(baseline.get("coverage"), {"complete", "curated"})
            or any(not isinstance(baseline.get(k), list) for k in ("terms", "relations"))
        ):
            return [*errors, "baseline needs coverage, terms and relations"]
        base_terms = baseline["terms"]
        base_relations = baseline["relations"]
        if any(
            not isinstance(x, dict)
            or not _text(x.get("id"))
            or not isinstance(x.get("labels"), list)
            or any(
                not isinstance(y, dict)
                or any(not _text(y.get(k)) for k in ("text", "language", "role"))
                for y in x["labels"]
            )
            for x in base_terms
        ):
            return [*errors, "baseline terms need ids and normalized labels"]
        if any(
            not isinstance(x, dict)
            or any(not _text(x.get(k)) for k in ("subject", "predicate", "object", "status"))
            for x in base_relations
        ):
            return [*errors, "baseline relations must be normalized identifier triples"]
        base = {x["id"]: x for x in base_terms}
        if len(base) != len(base_terms):
            errors.append("baseline has duplicate term ids")
        selected = set(indexed["terms"])
        if not selected <= set(base):
            errors.append("output invents or changes a source concept id")
        if baseline["coverage"] == "complete" and not set(base) <= selected:
            errors.append("complete output omits source concepts")
        for identity in selected & set(base):
            original, generated = base[identity], indexed["terms"][identity]
            if not _labels(original) <= _labels(generated):
                errors.append(f"term {identity} loses or changes a source label")
            if any(label[2] != "generated" for label in _labels(generated) - _labels(original)):
                errors.append(f"term {identity} adds an unsupplied label without generated status")
            if original.get("kind") and original["kind"] != generated.get("kind"):
                errors.append(f"term {identity} changes source kind")
        preserved = {
            _edge(x)
            for x in base_relations
            if x.get("status") == "asserted"
            and (x.get("subject") in selected or x.get("object") in selected)
        }
        if not preserved <= edges:
            errors.append(
                "output loses or changes an asserted source relation involving a selected term"
            )
        original_edges = {_edge(x) for x in base_relations if x.get("status") == "asserted"}
        if any(x[3] == "asserted" and x not in original_edges for x in edges):
            errors.append("output adds an asserted relation absent from the baseline")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("content", type=Path)
    parser.add_argument("--baseline", type=Path)
    args = parser.parse_args()
    try:
        content = json.loads(args.content.read_text(encoding="utf-8-sig"))
        baseline = (
            json.loads(args.baseline.read_text(encoding="utf-8-sig")) if args.baseline else None
        )
        errors = validate(content, baseline)
    except (OSError, ValueError) as error:
        parser.exit(2, f"Cannot read input: {error}\n")
    if errors:
        parser.exit(1, "\n".join(errors) + "\n")
    print(
        "Content structure and requested preservation checks passed; "
        "factual accuracy was not checked."
    )


if __name__ == "__main__":
    main()
