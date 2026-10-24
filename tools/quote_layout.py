"""Compatibility entry point: prepare current PETG/sample quotation files.

The old seven-PETG/two-TPU batches are historical, not current order quantities.
"""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from tools.prepare_print_order import build

if __name__=='__main__':
    build()
