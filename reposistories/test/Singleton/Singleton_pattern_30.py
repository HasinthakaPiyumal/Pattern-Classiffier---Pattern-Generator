class ResourceManagerFactory:
    _instance = None

    def __call__(self, resource_base_path="/app/resources"):
        if self._instance is None:
            self._instance = _ResourceManager(resource_base_path)
        return self._instance

class _ResourceManager:
    def __init__(self, base_path):
        self.base_path = base_path
        self.loaded_resources = {}

    def load_resource(self, resource_id, resource_type="image"):
        if resource_id not in self.loaded_resources:
            resource_path = f"{self.base_path}/{resource_id}.{resource_type}"
            self.loaded_resources[resource_id] = f"Loaded_{resource_type}_{resource_id}_from_{resource_path}"
        return self.loaded_resources[resource_id]

    def unload_resource(self, resource_id):
        if resource_id in self.loaded_resources:
            del self.loaded_resources[resource_id]
            return True
        return False

    def get_loaded_resources(self):
        return list(self.loaded_resources.keys())

if __name__ == "__main__":
    get_resource_manager = ResourceManagerFactory()

    rm1 = get_resource_manager("/game/assets")
    rm2 = get_resource_manager("/data/images")

    print(f"Are rm1 and rm2 the same instance? {rm1 is rm2}")
    print(f"RM1 base path: {rm1.base_path}")
    print(f"RM2 base path: {rm2.base_path}")

    rm1.load_resource("texture_grass", "png")
    rm2.load_resource("audio_impact", "wav")
    rm1.load_resource("font_arial", "ttf")

    print(f"Loaded resources: {rm1.get_loaded_resources()}")

    rm2.unload_resource("texture_grass")
    print(f"Loaded resources after unload: {rm1.get_loaded_resources()}")