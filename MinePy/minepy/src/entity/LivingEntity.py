from minepy.src.entity.Entity import Entity


class LivingEntity(Entity):
    entity_name = None

    def getName(self):
        return self.entity_name

    def setName(self, value: str):
        self.entity_name = value