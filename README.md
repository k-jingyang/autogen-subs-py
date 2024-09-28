# autogen-subs (Python)

Because getting it to work on Rust requires much more effort.

## Building it

```bash
docker build -t kjingyang/autogen-subs .
```

## Running it with Sonarr

- Must bind mount it with the data files used by Sonarr
  - The bind mounted path must also match Sonarr path
    - E.g. if a video file is `/x/y/z/video.mkv` in Sonarr, it must be `/x/y/z/video.mkv` in autogen-subs

## Benchmarks

Takes 14 minutes on mini-PC server for a 40 minute video
