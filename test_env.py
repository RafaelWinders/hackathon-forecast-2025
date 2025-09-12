#!/usr/bin/env python3
"""
Script para testar se todas as dependências estão funcionando corretamente
"""

print("Testando imports...")

try:
    import pandas as pd
    print(f"OK: pandas {pd.__version__}")
except ImportError as e:
    print(f"ERRO: pandas - {e}")

try:
    import numpy as np
    print(f"OK: numpy {np.__version__}")
except ImportError as e:
    print(f"ERRO: numpy - {e}")

try:
    import pickle
    print("OK: pickle")
except ImportError as e:
    print(f"ERRO: pickle - {e}")

try:
    import dask
    print(f"OK: dask {dask.__version__}")
except ImportError as e:
    print(f"ERRO: dask - {e}")

try:
    import sklearn
    print(f"OK: scikit-learn {sklearn.__version__}")
except ImportError as e:
    print(f"ERRO: scikit-learn - {e}")

try:
    import lightgbm as lgb
    print(f"OK: lightgbm {lgb.__version__}")
except ImportError as e:
    print(f"ERRO: lightgbm - {e}")

print("\nTeste concluido!")
print("Se todos os imports estao OK, seu ambiente esta pronto!")