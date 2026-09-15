os.environ["BYPO_APP_VARIANT"] = "bypo_cfg"

from bypo import start_machina

if __name__ == "__main__":
    start_machina("bypo_cfg")
