import random
from panda3d.core import (
    CardMaker,
    AmbientLight,
    DirectionalLight,)
from src import settings

class World:
    def __init__(self, game):
        self.game = game

        self._create_lights()
        self._create_ground()
        self._load_trees()

    def _create_lights(self):
        dlight = DirectionalLight("sun")
        dlight.setColor((1, 1, 1, 1))

        dlnp = self.game.render.attachNewNode(dlight)
        dlnp.setHpr(45, -45, 0)

        self.game.render.setLight(dlnp)

        alight = AmbientLight("ambient")
        alight.setColor((0.45, 0.45, 0.45, 1))
        alnp = self.game.render.attachNewNode(alight)
        self.game.render.setLight(alnp)

    def _create_ground(self):
        card = CardMaker("ground")
        size = settings.GROUND_SIZE
        card.setFrame(
            -size,
             size,
            -size,
             size
        )
        ground = self.game.render.attachNewNode(card.generate())
        ground.setP(-90)
        ground.setColor(0.18, 0.55, 0.18, 1)

    def _load_trees(self):
        for x in range( -settings.TREE_AREA, settings.TREE_AREA + 1, settings.TREE_SPACING):
            for y in range(-settings.TREE_AREA, settings.TREE_AREA + 1, settings.TREE_SPACING):
                tree_x = x + random.uniform(-3, 3)
                tree_y = y + random.uniform(-3, 3)
                if abs(tree_x) < 8 and abs(tree_y) < 8:
                    continue
                tree = self.game.loader.loadModel("models/trees/tree.gltf")
                tree.reparentTo(self.game.render)
                tree.setPos(tree_x, tree_y, 0)
                tree.setScale(settings.TREE_SCALE * random.uniform(0.8, 1.3))
                tree.setH(random.uniform(0, 360))
                tree.setP(90)