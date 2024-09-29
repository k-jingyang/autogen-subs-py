# autogen-subs (Python)

Because getting it to work on Rust requires much more effort.

## Building it

```bash
docker build -t kjingyang/autogen-subs .
```

## Usage

Sonarr

> So that we can autogenerate subtitles for imported TV shows

1. Must bind mount it with the data files used by Sonarr
  - The bind mounted path must also match Sonarr path
    - E.g. if a video file is `/x/y/z/video.mkv` in Sonarr, it must be `/x/y/z/video.mkv` in autogen-subs

Bazarr

> Skip if not using Bazarr. To prevent the auto generated subs from overwriting subs downloaded by Bazarr.

1. Disable Single Language option in Bazarr, under Settings > Languages

## Benchmarks

Takes 14 minutes for a 40 minute video on a VM with the following specs
- 2 sockets, 2 core (Physical host CPU: i5-8500T CPU)
- 12 GB RAM

## References

https://www.scaleway.com/en/blog/ai-in-practice-generating-video-subtitles/