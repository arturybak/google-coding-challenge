"""A video player class."""
import random

from .video_library import VideoLibrary, VideoLibraryError
from .video_playback import VideoPlayback, PlaybackState, VideoPlaybackError
from .video_playlist import PlaylistError, Playlist


class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self._playback = VideoPlayback()
        self._playlists = {}

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        print("Here's a list of all available videos:")
        for v in self._video_library.get_all_videos():
            print(v)

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        try:
            video = self._video_library[video_id]
        except VideoLibraryError as e:
            print(f"Cannot play video: {e}")
            return
        if self._playback.state != PlaybackState.STOPPED:
            self.stop_video()
        if video.flag:
            print(f"Cannot play video: Video is currently flagged (reason: {video.flag})")
            return
        self._playback.play(video)
        print(f"Playing video: {video.title}")

    def stop_video(self):
        """Stops the current video."""
        try:
            video = self._playback.get_video()
            print(f"Stopping video: {video.title}")
            self._playback.stop()
        except VideoPlaybackError as e:
            print(f"Cannot stop video: {e}")

    def play_random_video(self):
        """Plays a random video from the video library."""
        video = self._video_library.get_random_video_id()
        if video is None:
            print("No videos available")
        else:
            self.play_video(video)

    def pause_video(self):
        """Pauses the current video."""
        try:
            video = self._playback.get_video()
        except VideoPlaybackError as e:
            print(f"Cannot pause video: {e}")
            return

        if self._playback.state == PlaybackState.PAUSED:
            print(f"Video already paused: {video.title}")
        else:
            print(f"Pausing video: {video.title}")
            self._playback.pause()
        return

    def continue_video(self):
        """Resumes playing the current video."""

        try:
            video = self._playback.get_video()
        except VideoPlaybackError as e:
            print(f"Cannot continue video: {e}")
            return
        if self._playback.state != PlaybackState.PAUSED:
            print("Cannot continue video: Video is not paused")
        else:
            print(f"Continuing video: {video.title}")
            self._playback.play(video)
        return

    def show_playing(self):
        """Displays video currently playing."""

        try:
            video = self._playback.get_video()
        except VideoPlaybackError as e:
            print(f"Cannot get information on currently playing video: {e}")
            return
        state = self._playback.state
        if state == PlaybackState.STOPPED:
            print("No video is currently playing")
        else:
            print(f"Currently playing: {video}" + (" - PAUSED" if state == PlaybackState.PAUSED else ""))

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        # removing whitespace
        playlist_name = ''.join(playlist_name.split())

        if playlist_name.lower() in self._playlists:
            print("Cannot create playlist: A playlist with the same name already exists")
            return

        self._playlists[playlist_name.lower()] = Playlist(playlist_name)
        print(f"Successfully created new playlist: {playlist_name}")

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        video = self._video_library.get_video(video_id)

        # finding the playlist

        # any(p.name.lower() == playlist_name.lower() for p in self._playlists)
        # playlist = next((p for p in self._playlists if p.name.lower() == playlist_name.lower()), None)

        if playlist_name.lower() not in self._playlists:
            print(f"Cannot add video to {playlist_name}: Playlist does not exist")
            return
        if not video:
            print(f"Cannot add video to {playlist_name}: Video does not exist")
            return
        if video.flag:
            print(f"Cannot add video to {playlist_name}: Video is currently flagged (reason: {video.flag})")
            return
        playlist = self._playlists[playlist_name.lower()]
        if video in playlist.videos:
            print(f"Cannot add video to {playlist_name}: Video already added")
            return
        playlist.videos.append(video)
        print(f"Added video to {playlist_name}: {video.title}")

    def show_all_playlists(self):
        """Display all playlists."""

        if len(self._playlists) == 0:
            print("No playlists exist yet")
        else:
            print("Showing all playlists:")
            for playlist in sorted(self._playlists):
                print(f"  {self._playlists[playlist].name}")
        return

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.lower() not in self._playlists:
            print(f"Cannot show playlist {playlist_name}: Playlist does not exist")
            return
        playlist = self._playlists[playlist_name.lower()]
        print(f"Showing playlist: {playlist_name}")
        if not playlist.videos:
            print(f"No videos here yet")
            return
        for v in playlist.videos:
            print(v)

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        video = self._video_library.get_video(video_id)

        if playlist_name.lower() not in self._playlists:
            print(f"Cannot remove video from {playlist_name}: Playlist does not exist")
            return
        if not video:
            print(f"Cannot remove video from {playlist_name}: Video does not exist")
            return
        playlist = self._playlists[playlist_name.lower()]
        if video not in playlist.videos:
            print(f"Cannot remove video from {playlist_name}: Video is not in playlist")
            return
        playlist.videos.remove(video)
        print(f"Removed video from {playlist_name}: {video.title}")

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.lower() not in self._playlists:
            print(f"Cannot clear playlist {playlist_name}: Playlist does not exist")
            return
        playlist = self._playlists[playlist_name.lower()]
        playlist.videos.clear()
        print(f"Successfully removed all videos from {playlist_name}")

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.lower() not in self._playlists:
            print(f"Cannot delete playlist {playlist_name}: Playlist does not exist")
            return
        del self._playlists[playlist_name.lower()]
        print(f"Deleted playlist: {playlist_name}")

    def _search_general(self, query, result):
        ordered = sorted(result, key=lambda v: v.title)
        if not ordered:
            print(f"No search results for {query}")
            return
        print(f"Here are the results for {query}:")
        for i in range(len(ordered)):
            print(f"{i + 1}) {ordered[i]}")
        print("Would you like to play any of the above? If yes, specify the number of the video.\nIf your "
              "answer is not a valid number, we will assume it's a no.")
        answer = input()
        if not answer.isnumeric():
            return
        ans = int(answer)
        if 0 < ans <= len(ordered):
            self.play_video(ordered[ans - 1].video_id)

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        self._search_general(search_term,
                             filter(lambda v: search_term.lower() in v.title.lower(),
                                    self._video_library.get_unflagged_videos()))

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        self._search_general(video_tag,
                             filter(lambda v: video_tag.lower() in {t.lower() for t in v.tags},
                                    self._video_library.get_unflagged_videos()))

    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        try:
            video = self._video_library[video_id]
        except VideoLibraryError as e:
            print(f"Cannot flag video: {e}")
            return
        if not video:
            print("Cannot flag video: Video does not exist")
            return
        if video.flag:
            print("Cannot flag video: Video is already flagged")
            return
        flag_reason = "Not supplied" if not flag_reason else flag_reason
        if self._playback.state != PlaybackState.STOPPED:
            if self._playback.get_video() == video:
                self.stop_video()
        video.flag = flag_reason
        print(f"Successfully flagged video: {video.title} (reason: {flag_reason})")

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        try:
            video = self._video_library[video_id]
        except VideoLibraryError as e:
            print(f"Cannot remove flag from video: {e}")
            return
        if not video:
            print("Cannot remove flag from video: Video does not exist")
            return
        if not video.flag:
            print("Cannot remove flag from video: Video is not flagged")
            return
        video.flag = None

        print(f"Successfully removed flag from video: {video.title}")
