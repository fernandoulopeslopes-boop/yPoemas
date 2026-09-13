# =============================================================================
# bypo_cfg.py — BYPO_CFG / MACHINA HORIZONTAL + PÁGINA Z / TOOLS
# Build 2026-09-13_002 — curadoria ABOUT + ícone construction
#
# - Reusa integralmente bypo.py.
# - Acrescenta exclusivamente a Página Z / TOOLS.
# - ABOUT de curadoria: lista todos os /ypo/md_files/*.md.
# - Ícone próprio: :construction:.
# - Uso LOCAL ou WWW não público.
# =============================================================================

import os

os.environ["BYPO_APP_VARIANT"] = "bypo_cfg"

from bypo import start_machina


if __name__ == "__main__":
    start_machina("bypo_cfg")
