import logging
from moonraker.plugins import BasePlugin

LOG = logging.getLogger("moonraker.afc")

class AFCPlugin(BasePlugin):
    def __init__(self, config):
        super().__init__(config)
        self.server = config.get_server()
        self._init_state()
        self._register_endpoints()

    # -----------------------------
    # AFC STATE MODEL
    # -----------------------------
    def _init_state(self):
        self.state = {
            "status": "idle",          # idle, loading, unloading, error
            "active_slot": 0,
            "slots": [
                {"index": 0, "name": "Slot 1", "color": "#ff0000", "material": "PLA", "loaded": True},
                {"index": 1, "name": "Slot 2", "color": "#00ff00", "material": "PETG", "loaded": False},
                {"index": 2, "name": "Slot 3", "color": "#0000ff", "material": "ABS", "loaded": False},
                {"index": 3, "name": "Slot 4", "color": "#ffff00", "material": "PLA", "loaded": False},
            ],
            "error": None,
        }

    # -----------------------------
    # REGISTER API ENDPOINTS
    # -----------------------------
    def _register_endpoints(self):
        self.server.register_endpoint("/machine/afc/status", ["GET"], self._handle_status)
        self.server.register_endpoint("/machine/afc/load", ["POST"], self._handle_load)
        self.server.register_endpoint("/machine/afc/unload", ["POST"], self._handle_unload)
        self.server.register_endpoint("/machine/afc/select_slot", ["POST"], self._handle_select_slot)
        self.server.register_endpoint("/machine/afc/reset_error", ["POST"], self._handle_reset_error)

    # -----------------------------
    # ENDPOINT HANDLERS
    # -----------------------------
    async def _handle_status(self, req):
        return self.state

    async def _handle_load(self, req):
        data = await req.json()
        slot = int(data.get("slot", self.state["active_slot"]))
        self.state["status"] = "loading"
        self.state["active_slot"] = slot
        self._notify()
        return {"result": "ok"}

    async def _handle_unload(self, req):
        self.state["status"] = "unloading"
        self._notify()
        return {"result": "ok"}

    async def _handle_select_slot(self, req):
        data = await req.json()
        self.state["active_slot"] = int(data["slot"])
        self._notify()
        return {"result": "ok"}

    async def _handle_reset_error(self, req):
        self.state["error"] = None
        self.state["status"] = "idle"
        self._notify()
        return {"result": "ok"}

    # -----------------------------
    # SEND EVENT TO MAINSAIL
    # -----------------------------
    def _notify(self):
        self.server.send_event("notify_afc_status_changed", self.state)

def load_plugin(config):
    return AFCPlugin(config)
