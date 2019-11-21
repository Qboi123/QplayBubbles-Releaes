from typing import Dict, Any


class Maintance:
    def __init__(self):
        pass

    @staticmethod
    def auto_save(save_name: str, game_stats: Dict[str, Any], bubble: Dict[str, Any]):
        """
        Saves the game. (For Auto-Save)
        """
        from .utils import config as cfg

        import os

        print(os.curdir)

        try:
            cfg.Writer("slots/" + save_name + "/game.data", game_stats.copy())
            cfg.Writer("slots/" + save_name + "/bubble.data", bubble.copy())
        except FileNotFoundError as e:
            print(e.args)
            print(e.filename)
            print(e.filename2)

    @staticmethod
    def auto_restore(save_name: str):
        """
        Restoring. (For Auto-Restore)
        """
        from .utils import config as cfg

        game_stats = cfg.Reader("slots/" + save_name + "/game.data").get_decoded()

        return game_stats

    @staticmethod
    def reset(save_name: str):
        """
        Resets the game fully
        """
        from .utils.get_set import get_root

        from .utils import config as cfg

        stats = cfg.Reader("versions/" + get_root().launcher_cfg["versionDir"] + "/config/reset.data").get_decoded()
        bubble = cfg.Reader(
            "versions/" + get_root().launcher_cfg["versionDir"] + "/config/reset-bubble.data").get_decoded()

        cfg.Writer("slots/" + save_name + "/game.data", stats.copy())
        cfg.Writer("slots/" + save_name + "/bubble.data", bubble.copy())
