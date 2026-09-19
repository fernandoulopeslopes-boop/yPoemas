# =============================================================================
# bypo_cfg.py — BYPO_CFG / oficina privada + página Z / TOOLS
# Build 2026-09-19_005 — entrada CFG do motor BYPO 053
#
# - Porta de trabalho LOCAL: importa o motor irmão bypo.py.
# - Solicita explicitamente a variante bypo_cfg (com Z/TOOLS).
# - Não publica a página Z na entrada pública bypo.py.
# =============================================================================

import os

os.environ["BYPO_APP_VARIANT"] = "bypo_cfg"

from bypo import start_machina


if __name__ == "__main__":
    start_machina("bypo_cfg")
