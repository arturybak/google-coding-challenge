"""A video playlist class."""


class PlaylistError(Exception):
    pass


class Playlist:
    """A class used to represent a Playlist."""
    def __init__(self, name):
        self.name = name
        self.videos = []
