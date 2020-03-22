from tkinter import Tk, PhotoImage
from typing import Callable, Type, Any, List

from PIL import ImageTk

from base import Bubble
from gameIO import printerr


class Registry(object):
    saveConfig = {}
    saveData = {}
    gameConfig = {}
    gameData = {}

    _registryScenes = {}
    _registryBubble = {}
    _registrySprite = {}
    _registryKeyBind = {}
    _registryXboxBind = {}
    _registryImage = {}
    _registryForeground = {}
    _registryBackground = {}
    _registryIcon = {}
    _registryStoreIcon = {}
    _registryRoot: Tk = None

    @classmethod
    def get_scene(cls, name):
        return cls._registryScenes[name]

    @classmethod
    def get_bubble(cls, id):
        return cls._registryBubble[id]

    @classmethod
    def get_keybinding(cls, key):
        return cls._registryKeyBind[key]

    @classmethod
    def get_xboxbinding(cls, key):
        return cls._registryXboxBind[key]

    @classmethod
    def get_root(cls) -> Tk:
        return cls._registryRoot

    @classmethod
    def register_scene(cls, name: str, scene: Type[Callable]):
        if type(name) != str:
            raise TypeError(f"Scene name must be a str-object not "
                             f"{'an' if name.__class__.__name__.startswith(('e', 'a', 'i', 'o', 'u')) else 'a'} "
                             f"{type(name)}-object")
        # printerr(f"{repr(scene)} is not a SceneObject Representaion")
        if not (repr(scene).startswith("SceneObject<") and repr(scene).endswith(">")):
            raise ValueError(f"Representation is not of a Scene-object, or is this not a subclass of a Scene-object?")
        cls._registryScenes[name] = scene

    @classmethod
    def register_bubble(cls, id: str, bubbleobj: Bubble):
        if type(id) != str:
            raise TypeError(f"Bubble ID must be a str-object not "
                             f"{'an' if id.__class__.__name__.startswith(('e', 'a', 'i', 'o', 'u')) else 'a'} "
                             f"{type(id)}-object")
        cls._registryBubble[id] = bubbleobj

    @classmethod
    def register_keybinding(cls, key: str, command: Callable):
        if type(key) != str:
            raise TypeError(f"Key-binding must be a str-object not "
                             f"{'an' if key.__class__.__name__.startswith(('e', 'a', 'i', 'o', 'u')) else 'a'} "
                             f"{type(id)}-object")

        if key in cls._registryXboxBind:
            printerr(f"Key-binding with key '{key}' already exists!")
        cls._registryKeyBind[key] = command

    @classmethod
    def register_xboxbinding(cls, key: str, command: Callable):
        if type(key) != str:
            raise TypeError(
                f"Xbox-binding must be a str-object not "
                f"{'an' if key.__class__.__name__.startswith(('e', 'a', 'i', 'o', 'u')) else 'a'} "
                f"{type(id)}-object")

        if key in cls._registryXboxBind:
            printerr(f"Xbox-binding with key '{key}' already exists!")
        cls._registryXboxBind[key] = command

    @classmethod
    def register_root(cls, window):
        if not issubclass(type(window), Tk):
            raise TypeError(
                f"Xbox-binding must be a subclass of a Tk-object not "
                f"{'an' if window.__class__.__name__.startswith(('e', 'a', 'i', 'o', 'u')) else 'a'} "
                f"{type(id)}-object, wich is not subclass of a Tk-object")

        if cls._registryRoot is not None:
            printerr(f"Root already exists!")
        cls._registryRoot = window

    @classmethod
    def register_image(cls, name, image: PhotoImage):
        if type(name) != str:
            raise TypeError(
                f"Image name must be a str-object not "
                f"{'an' if name.__class__.__name__.startswith(('e', 'a', 'i', 'o', 'u')) else 'a'} "
                f"{type(id)}-object")
        if type(image) != PhotoImage:
            if type(image) != ImageTk.PhotoImage:
                raise TypeError(
                    f"Image must be a PhotoImage-object not "
                    f"{'an' if name.__class__.__name__.startswith(('e', 'a', 'i', 'o', 'u')) else 'a'} "
                    f"{type(id)}-object")

        if name in cls._registryXboxBind:
            printerr(f"Image with name '{name}' already exists!")
        cls._registryImage[name] = image

    @classmethod
    def register_foreground(cls, name, image: PhotoImage):
        if type(name) != str:
            raise TypeError(
                f"Foreground name must be a str-object not "
                f"{'an' if name.__class__.__name__.startswith(('e', 'a', 'i', 'o', 'u')) else 'a'} "
                f"{type(id)}-object")
        if type(image) != PhotoImage:
            if type(image) != ImageTk.PhotoImage:
                raise TypeError(
                    f"Foreground image must be a PhotoImage-object not "
                    f"{'an' if name.__class__.__name__.startswith(('e', 'a', 'i', 'o', 'u')) else 'a'} "
                    f"{type(id)}-object")

        if name in cls._registryXboxBind:
            printerr(f"Foreground with name '{name}' already exists!")
        cls._registryForeground[name] = image

    @classmethod
    def register_background(cls, name, image: PhotoImage):
        if type(name) != str:
            raise TypeError(
                f"Background name must be a str-object not "
                f"{'an' if name.__class__.__name__.startswith(('e', 'a', 'i', 'o', 'u')) else 'a'} "
                f"{type(id)}-object")
        if type(image) != PhotoImage:
            if type(image) != ImageTk.PhotoImage:
                raise TypeError(
                    f"Background image must be a PhotoImage-object not "
                    f"{'an' if name.__class__.__name__.startswith(('e', 'a', 'i', 'o', 'u')) else 'a'} "
                    f"{type(id)}-object")

        if name in cls._registryXboxBind:
            printerr(f"Image with name '{name}' already exists!")
        cls._registryBackground[name] = image

    @classmethod
    def register_storeitem(cls, name, icon: PhotoImage, obj: Callable = None):
        if type(name) != str:
            raise TypeError(
                f"Store item name must be a str-object not "
                f"{'an' if name.__class__.__name__.startswith(('e', 'a', 'i', 'o', 'u')) else 'a'} "
                f"{type(id)}-object")
        if type(icon) != PhotoImage:
            if type(icon) != ImageTk.PhotoImage:
                raise TypeError(
                    f"Store item icon must be a PhotoImage-object not "
                    f"{'an' if name.__class__.__name__.startswith(('e', 'a', 'i', 'o', 'u')) else 'a'} "
                    f"{type(id)}-object")

        # # TODO: Make store item objects compatible
        # # printerr(f"{repr(scene)} is not a SceneObject Representaion")
        # if not (repr(obj).startswith("StoreItem<") and repr(obj).endswith(">")):
        #     raise ValueError(f"Representation is not of a StoreItem-object, or is this not a subclass of a Scene-object?")
        if name in cls._registryXboxBind:
            printerr(f"Store item icon with name '{name}' already exists!")
        cls._registryStoreIcon[name] = icon

    @classmethod
    def register_icon(cls, name, image: PhotoImage):
        if type(name) != str:
            raise TypeError(
                f"Icon name must be a str-object not "
                f"{'an' if name.__class__.__name__.startswith(('e', 'a', 'i', 'o', 'u')) else 'a'} "
                f"{type(id)}-object")
        if type(image) != PhotoImage:
            if type(image) != ImageTk.PhotoImage:
                raise TypeError(
                    f"Icon image must be a PhotoImage-object not "
                    f"{'an' if name.__class__.__name__.startswith(('e', 'a', 'i', 'o', 'u')) else 'a'} "
                    f"{type(id)}-object")

        if name in cls._registryXboxBind:
            printerr(f"Ìcon with name '{name}' already exists!")
        cls._registryIcon[name] = image
