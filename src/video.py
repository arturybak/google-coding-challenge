"""A video class."""

from typing import Sequence, Optional


class Video:
    """A class used to represent a Video."""

    def __init__(self, video_title: str, video_id: str, video_tags: Sequence[str]):
        """Video constructor."""
        self._title = video_title
        self._video_id = video_id
        self._flag = None

        # Turn the tags into a tuple here so it's unmodifiable,
        # in case the caller changes the 'video_tags' they passed to us
        self._tags = tuple(video_tags)

    @property
    def title(self) -> str:
        """Returns the title of a video."""
        return self._title

    @property
    def video_id(self) -> str:
        """Returns the video id of a video."""
        return self._video_id

    @property
    def tags(self) -> Sequence[str]:
        """Returns the list of tags of a video."""
        return self._tags

    @property
    def flag(self) -> Optional[str]:
        """Returns the the flag status of a video."""
        return self._flag

    @flag.setter
    def flag(self, reason=""):
        self._flag = reason

    @property
    def tags_string(self) -> str:
        """Returns the tags as a string"""
        return ' '.join(self.tags)

    def __str__(self):
        """a toString method
        """
        result = f'{self.title} ({self.video_id}) [{self.tags_string}]' + (f' - FLAGGED (reason: {self.flag})' if self.flag else '')
        return result
