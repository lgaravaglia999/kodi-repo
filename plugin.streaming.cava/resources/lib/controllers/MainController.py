from resources.lib import kodiutilsitem
from resources.lib.streaming_hosts import speedvideo, openload
from resources.lib import kodiplayer


def play(title, streaming_url):
    streaming_source_name = kodiutilsitem.get_streaming_source_name(streaming_url)

    if streaming_source_name == "speedvideo":
        playable_url = speedvideo.get_stream_url(streaming_url)
        if streaming_url != '' and streaming_url != '404':
            kodiplayer.play_video(playable_url, addon_handle)

    elif streaming_source_name == "openload":
        kodiplayer.play_video_with_resolver(streaming_url, addon_handle)
    
    elif streaming_source_name == "rapidcrypt":
        playable_url = openload.get_openload(streaming_url)
        kodiplayer.play_video_with_resolver(playable_url, addon_handle)
