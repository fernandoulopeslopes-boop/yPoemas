# =============================================================================
# bypo_cfg.py — BYPO_CFG / MACHINA HORIZONTAL + PÁGINA Z / TOOLS
# Build 2026-09-13_002 — launcher dedicado / ícone próprio
#
# - Define a variante antes de importar bypo.py.
# - Reusa integralmente o BYPO build 048.
# - Acrescenta exclusivamente a Página Z / TOOLS.
# - page_icon do CFG = :construction:.
# =============================================================================

import os

os.environ["BYPO_APP_VARIANT"] = "bypo_cfg"

from bypo import start_machina


if __name__ == "__main__":
    start_machina("bypo_cfg")
