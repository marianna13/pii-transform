"""
Test the PiiSubstitutionValue class
"""

from pathlib import Path
from os import unlink

import tempfile
import pytest

from typing import Dict

from pii_data.helper.exception import InvArgException, UnimplementedException
from pii_data.types import PiiEnum, PiiEntity
from pii_data.types.localdoc import BaseLocalSrcDocument, LocalSrcDocumentFile
from pii_data.types.piicollection import PiiCollectionLoader
from pii_data.helper.io import load_yaml

import pii_transform.api.transform as mod


DATADIR = Path(__file__).parents[2] / "data"


def save_load(doc: BaseLocalSrcDocument) -> Dict:
    try:
        f = tempfile.NamedTemporaryFile(mode="wt", suffix=".yml", delete=False)
        doc.dump(f, format="yml")
        f.close()
        return load_yaml(f.name)
    finally:
        Path(f.name).unlink()


# -----------------------------------------------------------------------


def test10_constructor():
    """
    Test constructing the object
    """
    m = mod.PiiTransformer()
    assert str(m) == "<PiiTransformer>"


def test20_process_seq():
    """
    """
    doc = LocalSrcDocumentFile(DATADIR / "minidoc-example-seq-orig.yaml")
    pii = PiiCollectionLoader()
    pii.load_json(DATADIR / "minidoc-example-seq-pii.json")
    m = mod.PiiTransformer()
    result = m(doc, pii)

    got = save_load(result)
    exp = load_yaml(DATADIR / "minidoc-example-seq-repl.yaml")
    assert exp == got


def test30_process_tree():
    """
    """
    doc = LocalSrcDocumentFile(DATADIR / "minidoc-example-tree-orig.yaml")
    pii = PiiCollectionLoader()
    pii.load_json(DATADIR / "minidoc-example-tree-pii.json")
    m = mod.PiiTransformer()
    result = m(doc, pii)

    got = save_load(result)
    exp = load_yaml(DATADIR / "minidoc-example-tree-repl.yaml")
    assert exp == got


def test40_process_table():
    """
    """
    doc = LocalSrcDocumentFile(DATADIR / "minidoc-example-table-orig.yaml")
    pii = PiiCollectionLoader()
    pii.load_json(DATADIR / "minidoc-example-table-pii.json")
    m = mod.PiiTransformer()
    result = m(doc, pii)

    got = save_load(result)
    exp = load_yaml(DATADIR / "minidoc-example-table-repl.yaml")
    assert exp == got
    
