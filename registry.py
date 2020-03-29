from tkinter import Tk, PhotoImage, Toplevel
from typing import Callable, Type, Any, List, Union

from PIL import ImageTk

from exceptions import UnlocalizedNameError
from gameIO import printerr, printwrn


class Registry(object):
    saveConfig = {}
    saveData = {}
    gameConfig = {}
    gameData = {}

    _registryScenes = {}
    _registrySceneManager = None
    _registryModes = {}
    _registryModeManager = None
    _registryBubbles = {}
    _registrySprites = {}
    _registryKeyBinds = {}
    _registryXboxBinds = {}
    _registryImages = {}
    _registryForegrounds = {}
    _registryBackgrounds = {}
    _registryIcons = {}
    _registryStoreIcons = {}
    _registryBubResources = {}
    _registryTextures = {}
    _registryRoot: Tk = None

    @classmethod
    def get_scene(cls, name):
        return cls._registryScenes[name]

    @classmethod
    def scene_exists(cls, name):
        return name in cls._registryScenes.keys()

    @classmethod
    def get_mode(cls, name):
        return cls._registryModes[name]

    @classmethod
    def mode_exists(cls, name):
        return name in cls._registryModes.keys()

    @classmethod
    def get_bubble(cls, id):
        return cls._registryBubbles[id]

    @classmethod
    def get_keybinding(cls, key):
        return cls._registryKeyBinds[key]

    @classmethod
    def get_xboxbinding(cls, key):
        return cls._registryXboxBinds[key]

    @classmethod
    def get_root(cls) -> Tk:
        return cls._registryRoot

    @classmethod
    def get_id_bubble(cls, bubble) -> List[str]:
        return [key for key, value in cls._registryBubbles if value == bubble]

    @classmethod
    def register_scene(cls, name: str, scene: Type[Callable]):
        if type(name) != str:
            raise TypeError(f"Scene name must be a str-object not "
                             f"{'an' if name.__class__.__name__.startswith(('e', 'a', 'i', 'o', 'u')) else 'a'} "
                             f"{name.__class__.__name__}-object")
        # printerr(f"{repr(scene)} is not a SceneObject Representaion")
        if not (repr(scene).startswith("SceneObject<") and repr(scene).endswith(">")):
            raise ValueError(f"Representation is not of a Scene-object, or is this not a subclass of a Scene-object?")
        cls._registryScenes[name] = scene

    @classmethod
    def register_mode(cls, name: str, mode: object):
        if type(name) != str:
            raise TypeError(f"Mode name must be a str-object not "
                            f"{'an' if name.__class__.__name__.startswith(('e', 'a', 'i', 'o', 'u')) else 'a'} "
                            f"{name.__class__.__name__}-object")
        if not (repr(mode).startswith("ModeObject<") and repr(mode).endswith(">")):
            raise ValueError(f"Representation is not of a Mode-object, or is this not a subclass of a Mode-object?")
        cls._registryModes[name] = mode

    @classmethod
    def register_bubble(cls, id_: str, bubbleobj: object):
        if type(id_) != str:
            raise TypeError(f"Bubble ID must be a str-object not "
                             f"{'an' if id_.__class__.__name__.startswith(('e', 'a', 'i', 'o', 'u')) else 'a'} "
                             f"{id_.__class__.__name__}-object")
        if not (repr(bubbleobj).startswith("Bubble<") and repr(bubbleobj).endswith(">")):
            raise ValueError(f"Representation is not of a Bubble-object, or is this not a subclass of a Bubble-object?")
        cls._registryBubbles[id_] = bubbleobj

    @classmethod
    def register_keybinding(cls, key: str, command: Callable):
        if type(key) != str:
            raise TypeError(f"Key-binding must be a str-object not "
                             f"{'an' if key.__class__.__name__.startswith(('e', 'a', 'i', 'o', 'u')) else 'a'} "
                             f"{key.__class__.__name__}-object")

        if key in cls._registryXboxBinds:
            printerr(f"Key-binding with key '{key}' already exists!")
        cls._registryKeyBinds[key] = command

    @classmethod
    def register_xboxbinding(cls, key: str, command: Callable):
        if type(key) != str:
            raise TypeError(
                f"Xbox-binding must be a str-object not "
                f"{'an' if key.__class__.__name__.startswith(('e', 'a', 'i', 'o', 'u')) else 'a'} "
                f"{key.__class__.__name__}-object")

        if key in cls._registryXboxBinds:
            printerr(f"Xbox-binding with key '{key}' already exists!")
        cls._registryXboxBinds[key] = command

    @classmethod
    def register_root(cls, window):
        if not issubclass(type(window), Tk):
            raise TypeError(
                f"Root must be a subclass of a Tk-object not "
                f"{'an' if window.__class__.__name__.startswith(('e', 'a', 'i', 'o', 'u')) else 'a'} "
                f"{window.__class__.__name__}-object, wich is not subclass of a Tk-object")

        if cls._registryRoot is not None:
            printerr(f"Root already exists!")
        cls._registryRoot = window

    @classmethod
    def register_image(cls, name, image: PhotoImage):
        if type(name) != str:
            raise TypeError(
                f"Image name must be a str-object not "
                f"{'an' if name.__class__.__name__.startswith(('e', 'a', 'i', 'o', 'u')) else 'a'} "
                f"{name.__class__.__name__}-object")
        if type(image) != PhotoImage:
            if type(image) != ImageTk.PhotoImage:
                raise TypeError(
                    f"Image must be a PhotoImage-object not "
                    f"{'an' if image.__class__.__name__.startswith(('e', 'a', 'i', 'o', 'u')) else 'a'} "
                    f"{image.__class__.__name__}-object")

        if name in cls._registryImages.keys():
            printerr(f"Image with name '{name}' already exists!")
        cls._registryImages[name] = image

    @classmethod
    def register_foreground(cls, name, image: PhotoImage):
        if type(name) != str:
            raise TypeError(
                f"Foreground name must be a str-object not "
                f"{'an' if name.__class__.__name__.startswith(('e', 'a', 'i', 'o', 'u')) else 'a'} "
                f"{name.__class__.__name__}-object")
        if type(image) != PhotoImage:
            if type(image) != ImageTk.PhotoImage:
                raise TypeError(
                    f"Foreground image must be a PhotoImage-object not "
                    f"{'an' if image.__class__.__name__.startswith(('e', 'a', 'i', 'o', 'u')) else 'a'} "
                    f"{image.__class__.__name__}-object")

        if name in cls._registryXboxBinds:
            printerr(f"Foreground with name '{name}' already exists!")
        cls._registryForegrounds[name] = image

    @classmethod
    def register_background(cls, name, image: PhotoImage):
        if type(name) != str:
            raise TypeError(
                f"Background name must be a str-object not "
                f"{'an' if name.__class__.__name__.startswith(('e', 'a', 'i', 'o', 'u')) else 'a'} "
                f"{name.__class__.__name__}-object")
        if type(image) != PhotoImage:
            if type(image) != ImageTk.PhotoImage:
                raise TypeError(
                    f"Background image must be a PhotoImage-object not "
                    f"{'an' if image.__class__.__name__.startswith(('e', 'a', 'i', 'o', 'u')) else 'a'} "
                    f"{image.__class__.__name__}-object")

        if name in cls._registryXboxBinds:
            printerr(f"Image with name '{name}' already exists!")
        cls._registryBackgrounds[name] = image

    @classmethod
    def register_storeitem(cls, name, icon: PhotoImage, obj: Callable = None):
        if type(name) != str:
            raise TypeError(
                f"Store item name must be a str-object not "
                f"{'an' if name.__class__.__name__.startswith(('e', 'a', 'i', 'o', 'u')) else 'a'} "
                f"{name.__class__.__name__}-object")
        if type(icon) != PhotoImage:
            if type(icon) != ImageTk.PhotoImage:
                raise TypeError(
                    f"Store item icon must be a PhotoImage-object not "
                    f"{'an' if icon.__class__.__name__.startswith(('e', 'a', 'i', 'o', 'u')) else 'a'} "
                    f"{icon.__class__.__name__}-object")

        # # TODO: Make store item objects compatible
        # # printerr(f"{repr(scene)} is not a SceneObject Representaion")
        # if not (repr(obj).startswith("StoreItem<") and repr(obj).endswith(">")):
        #     raise ValueError(f"Representation is not of a StoreItem-object, or is this not a subclass of a Scene-object?")
        if name in cls._registryXboxBinds:
            printerr(f"Store item icon with name '{name}' already exists!")
        cls._registryStoreIcons[name] = icon

    @classmethod
    def register_icon(cls, name, image: PhotoImage):
        if type(name) != str:
            raise TypeError(
                f"Icon name must be a str-object not "
                f"{'an' if name.__class__.__name__.startswith(('e', 'a', 'i', 'o', 'u')) else 'a'} "
                f"{name.__class__.__name__}-object")
        if type(image) != PhotoImage:
            if type(image) != ImageTk.PhotoImage:
                raise TypeError(
                    f"Icon image must be a PhotoImage-object not "
                    f"{'an' if name.__class__.__name__.startswith(('e', 'a', 'i', 'o', 'u')) else 'a'} "
                    f"{image.__class__.__name__}-object")

        if name in cls._registryXboxBinds:
            printerr(f"Ìcon with name '{name}' already exists!")
        cls._registryIcons[name] = image

    @classmethod
    def get_bubresource(cls, uname, key):
        if uname not in cls._registryBubResources.keys():
            raise UnlocalizedNameError(f"bubble resource with unmame '{uname}' is non-existent")
        bub_reslist = cls._registryBubResources[uname]
        if key not in bub_reslist.keys():
            raise KeyError(f"key '{key}' for bubble resource '{uname}' is non-existent")
        bub_res = bub_reslist[key]
        return bub_res

    @classmethod
    def register_bubresource(cls, uname, key, value):
        if type(uname) != str:
            raise TypeError(
                f"uname for bubble resource must be a str-object not "
                f"{'an' if uname.__class__.__name__.startswith(('e', 'a', 'i', 'o', 'u')) else 'a'} "
                f"{uname.__class__.__name__}-object")
        if type(key) != str:
            raise TypeError(
                f"key for bubble resource must be a str-object not "
                f"{'an' if key.__class__.__name__.startswith(('e', 'a', 'i', 'o', 'u')) else 'a'} "
                f"{key.__class__.__name__}-object")

        if uname in cls._registryBubResources.keys():
            if key in cls._registryBubResources[uname].keys():
                printwrn(f"bubble resource key '{key}' with uname '{uname}' is overridden, this can be a intended override, "
                         f"but usually a mistake")
            cls._registryBubResources[uname][key] = value
        else:
            cls._registryBubResources[uname] = {key: value}

    @classmethod
    def get_texture(cls, type_, id_) -> Union[PhotoImage, ImageTk.PhotoImage]:
        if type_ not in cls._registryTextures.keys():
            raise KeyError(f"Type '{type_}' is not found in texture registry")
        if id_ not in cls._registryTextures[type_].keys():
            raise KeyError(f"ID '{id_}' with type '{type_}' is not found in texture registry")
        return cls._registryTextures[type_][id_]

    @classmethod
    def get_current_scene(cls):
        return cls.get_scene("Game").scenemanager.currentScene

    @classmethod
    def get_scenemanager(cls):
        return cls.get_scene("Game").scenemanager

    @classmethod
    def register_scenemanager(cls, scenemanager):
        if cls._registrySceneManager is not None:
            raise RuntimeError("scenemanager already registered")
        cls._registrySceneManager = scenemanager
    
    @classmethod
    def register_texture(cls, type_, id_, texture):
        if type(type_) != str:
            raise TypeError(
                f"Texture type must be a str-object not "
                f"{'an' if type_.__class__.__name__.startswith(('e', 'a', 'i', 'o', 'u')) else 'a'} "
                f"{type_.__class__.__name__}-object")
        if type(id_) != str:
            raise TypeError(
                f"Texture ID must be a str-object not "
                f"{'an' if id_.__class__.__name__.startswith(('e', 'a', 'i', 'o', 'u')) else 'a'} "
                f"{id_.__class__.__name__}-object")
        if type(texture) != PhotoImage:
            if type(texture) != ImageTk.PhotoImage:
                raise TypeError(
                    f"Image must be a PhotoImage-object not "
                    f"{'an' if texture.__class__.__name__.startswith(('e', 'a', 'i', 'o', 'u')) else 'a'} "
                    f"{texture.__class__.__name__}-object")

        if type_ in cls._registryTextures.keys():
            if id_ in cls._registryTextures[type_].keys():
                printwrn(f"texture with ID '{id_}' and type '{type_}' is overridden, this can be a intended override, "
                         f"but usually a mistake")
            cls._registryTextures[type_][id_] = texture
        else:
            cls._registryTextures[type_] = {id_: texture}
