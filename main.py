from fastapi import FastAPI
from os import path
from datetime import timedelta
from pathlib import Path
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
import logging
import whisper


model = whisper.load_model("base")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class SonarrSeries(BaseSchema):
    id: int
    title: str
    path: str  # folder path of the series


class SonarrEpisodeFile(BaseSchema):
    id: int
    relative_path: str
    path: str
    size: int
    scene_name: str


class SonarrImportHook(BaseSchema):
    series: SonarrSeries
    episode_file: SonarrEpisodeFile

    def get_imported_file_path(self) -> Path:
        return Path(self.series.path).joinpath(self.episode_file.relative_path)


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/sonarr_webhook")
async def transcribe_tv(hook: SonarrImportHook):
    file_path = hook.get_imported_file_path()
    thread = Thread(target=transcribe, args=(file_path))
    # run the thread
    thread.start()
    return {"status": "success"}


def transcribe(video_path: Path) -> str:
    audio = whisper.load_audio(video_path)

    logger.info("Transcribing video: %s", video_path)
    result = model.transcribe(audio)

    segments = result["segments"]

    video_dir = video_path.parent
    video_name = video_path.stem
    subtitle_file = f"{video_name}-llm-sub.srt"
    subtitle_path = video_dir.joinpath(subtitle_file)
    logger.info("Writing to subtitle file: %s", subtitle_path)

    # Write to subtitle file
    with open(subtitle_path, "w", encoding="utf-8") as srtFile:
        for segment in segments:
            startTime = str(0) + str(timedelta(seconds=int(segment["start"]))) + ",000"
            endTime = str(0) + str(timedelta(seconds=int(segment["end"]))) + ",000"
            text = segment["text"]

            subtitle_segment = (
                f"{segment['id'] + 1}\n{startTime} --> {endTime}\n{ text }\n\n"
            )

            srtFile.write(subtitle_segment)

    return subtitle_path.as_posix()
