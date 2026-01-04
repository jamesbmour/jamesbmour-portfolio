import { useEffect, useState } from 'react';
import axios from 'axios';
import { skeleton } from '../../utils';

interface Video {
  id: string;
  title: string;
  thumbnail: string;
  link: string;
  pubDate: string;
  description: string;
}

interface RssItem {
  guid: string;
  title: string;
  link: string;
  pubDate: string;
  description: string;
}

const LatestYoutube = ({ channelId }: { channelId: string }) => {
  const [videos, setVideos] = useState<Video[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    const fetchVideos = async () => {
      try {
        const rssUrl = `https://www.youtube.com/feeds/videos.xml?channel_id=${channelId}`;
        const response = await axios.get(
          `https://api.rss2json.com/v1/api.json?rss_url=${encodeURIComponent(rssUrl)}`,
        );

        if (response.data.status === 'ok') {
          const fetchedVideos = response.data.items
            .filter((item: RssItem) => !item.link.includes('/shorts/'))
            .slice(0, 6)
            .map((item: RssItem) => {
              // Extract video ID from link or guid if possible
              const videoId = item.guid.split(':')[2];
              return {
                id: videoId,
                title: item.title,
                thumbnail: `https://i.ytimg.com/vi/${videoId}/hqdefault.jpg`,
                link: item.link,
                pubDate: item.pubDate,
                description: item.description,
              };
            });
          setVideos(fetchedVideos);
        } else {
          setError(true);
        }
      } catch (err) {
        console.error('Failed to fetch YouTube videos', err);
        setError(true);
      } finally {
        setLoading(false);
      }
    };

    if (channelId) {
      fetchVideos();
    }
  }, [channelId]);

  if (error || (!loading && videos.length === 0)) return null;

  return (
    <div className="col-span-1 lg:col-span-2">
      <div className="grid grid-cols-1 gap-6">
        <div className="col-span-2">
          <div className="card compact bg-base-100 shadow bg-opacity-40">
            <div className="card-body">
              <div className="mx-3 mb-2 flex items-center justify-between">
                <h5 className="card-title">
                  {loading ? (
                    skeleton({ widthCls: 'w-28', heightCls: 'h-8' })
                  ) : (
                    <span className="text-base-content opacity-70">
                      Latest Videos
                    </span>
                  )}
                </h5>
                {loading ? (
                  skeleton({ widthCls: 'w-10', heightCls: 'h-5' })
                ) : (
                  <a
                    href={`https://www.youtube.com/channel/${channelId}`}
                    target="_blank"
                    rel="noreferrer"
                    className="text-base-content opacity-50 hover:underline"
                  >
                    See All
                  </a>
                )}
              </div>

              <div className="col-span-2">
                <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
                  {loading
                    ? Array.from({ length: 6 }).map((_, index) => (
                        <div
                          key={index}
                          className="card shadow-lg compact bg-base-100"
                        >
                          <div className="p-4">
                            {skeleton({
                              widthCls: 'w-full',
                              heightCls: 'h-32',
                              shape: 'rounded-lg',
                              className: 'mb-4',
                            })}
                            {skeleton({
                              widthCls: 'w-3/4',
                              heightCls: 'h-4',
                              shape: 'rounded-lg',
                              className: 'mb-2',
                            })}
                            {skeleton({
                              widthCls: 'w-1/2',
                              heightCls: 'h-4',
                              shape: 'rounded-lg',
                            })}
                          </div>
                        </div>
                      ))
                    : videos.map((video) => (
                        <a
                          key={video.id}
                          href={video.link}
                          target="_blank"
                          rel="noreferrer"
                          className="card shadow-lg compact bg-base-100 cursor-pointer hover:shadow-xl transition-shadow duration-200"
                        >
                          <div className="p-4">
                            <div className="relative aspect-video w-full overflow-hidden rounded-lg bg-base-200 mb-4">
                              <img
                                src={video.thumbnail}
                                alt={video.title}
                                className="h-full w-full object-cover"
                                loading="lazy"
                              />
                            </div>
                            <div className="flex flex-col">
                              <h2 className="font-semibold text-base-content opacity-60 line-clamp-1 mb-1">
                                {video.title}
                              </h2>
                              <p className="text-xs opacity-50 text-base-content mb-2">
                                {new Date(video.pubDate).toLocaleDateString(
                                  undefined,
                                  {
                                    year: 'numeric',
                                    month: 'short',
                                    day: 'numeric',
                                  },
                                )}
                              </p>
                              <p className="text-sm text-base-content text-opacity-60 line-clamp-2">
                                {video.description}
                              </p>
                            </div>
                          </div>
                        </a>
                      ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LatestYoutube;
