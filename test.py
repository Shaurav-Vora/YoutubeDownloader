from pytubefix import YouTube, Channel, Playlist, Search

yt = YouTube("https://www.youtube.com/watch?v=p9ok7YYWNXI&ab_channel=SidemenReacts")
yt_year = yt.publish_date.date().year
yt_likes = yt.likes
print(yt.streams.filter(only_audio=True))

p = Playlist("https://www.youtube.com/watch?v=O93hwvz4_HA&list=PLhjLcvbbPVrVJdOqNgMbe_O9qlWplCsiQ&ab_channel=MoreSidemen")
p.length

print(yt_year, f"{int(yt_likes) :,}")





# https://www.youtube.com/watch?v=9bZkp7q19f0