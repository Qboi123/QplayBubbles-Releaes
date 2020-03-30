from typing import NoReturn

from base import Sprite
from effects import BaseEffect, AppliedEffect
from events import KeyPressEvent, KeyReleaseEvent, UpdateEvent, SavedataReadedEvent, ExperienceEvent
from registry import Registry
from sprite.abilities import GhostAbility


class Player(Sprite):
    def __init__(self):
        super(Player, self).__init__()

        self.appliedEffects = []
        self.appliedEffectTypes = []

        self.score = 0
        self.health = 10
        self.maxHealth = 10
        self._exp = 0

        self.baseSpeed = 0

        self.keysPressed = ""
        self._spriteName = "player"

    def add_effect(self, effect):
        self.appliedEffects.append(effect)
        self.appliedEffectTypes.append(type(effect))

    def activate_events(self):
        KeyPressEvent.bind(self.on_key_press)
        KeyReleaseEvent.bind(self.on_key_release)
        UpdateEvent.bind(self.on_update)
        SavedataReadedEvent.bind(self.on_savedata_readed)

    def deactivate_events(self):
        KeyPressEvent.unbind(self.on_key_press)
        KeyReleaseEvent.unbind(self.on_key_release)
        UpdateEvent.unbind(self.on_update)
        SavedataReadedEvent.unbind(self.on_savedata_readed)

    def add_experience(self, experience):
        ExperienceEvent(self, experience)

    def on_savedata_readed(self, data):
        self.score = data["Player"]["score"]

        for effect in data["Player"]["Effects"]:
            effect_class: BaseEffect = Registry.get_effect(effect["id"])
            time_length: float = effect["timeRemaining"]
            strength: float = effect["strength"]
            self.start_effect(effect_class, Registry.get_scene("Game"), time_length, strength)

    def start_effect(self, effect_class, scene, time_length, strength) -> NoReturn:
        self.appliedEffects.append(AppliedEffect(effect_class, scene, time_length, strength))

    def move(self, x=0, y=0):
        Registry.get_scene("Game").canvas.move(self.id, x, y)

    def move_joy(self, x=0, y=0):
        Registry.get_scene("Game").canvas.move(self.id, x, y)

    def on_update(self, evt: UpdateEvent):
        x, y = 0, 0
        if "w" in self.keysPressed:
            y -= self.baseSpeed
        if "a" in self.keysPressed:
            x -= self.baseSpeed
        if "s" in self.keysPressed:
            y += self.baseSpeed
        if "d" in self.keysPressed:
            x += self.baseSpeed
        self.move(x, y)

    def create(self, x, y):
        self.id = Registry.get_scene("Game").canvas.create_image(x, y, image=Registry.get_texture("sprite", "player", rotation=0))

    def on_key_press(self, evt: KeyPressEvent):
        if (evt.char.lower() == "w") and ("w" not in self.keysPressed):
            self.keysPressed += "w"
        elif (evt.char.lower() == "a") and ("a" not in self.keysPressed):
            self.keysPressed += "a"
        elif (evt.char.lower() == "s") and ("s" not in self.keysPressed):
            self.keysPressed += "s"
        elif (evt.char.lower() == "d") and ("d" not in self.keysPressed):
            self.keysPressed += "d"

    def on_key_release(self, evt: KeyReleaseEvent):
        a = list(self.keysPressed)
        if (evt.char.lower() == "w") and ("w" in self.keysPressed):
            a.remove("w")
        elif (evt.char.lower() == "a") and ("a" in self.keysPressed):
            a.remove("a")
        elif (evt.char.lower() == "s") and ("s" in self.keysPressed):
            a.remove("s")
        elif (evt.char.lower() == "d") and ("d" in self.keysPressed):
            a.remove("d")
        self.keysPressed = "".join(a)


class TeleportCrossbar(Sprite):
    def __init__(self):
        super(TeleportCrossbar, self).__init__()

        self.abilities.append(GhostAbility(self))
        self.abilities.append(InvulnerableAbility(self))

    def create(self, x, y):
        super(x, y)

    def on_key_release(self, evt: KeyReleaseEvent):
        if evt.keySym.lower() == "return":
            Registry.get_mode("teleport").execute("done", x=self.get_coords()[0], y=self.get_coords()[1])
