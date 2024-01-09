# RecordPlus
The project is a REST API using python django to consume endpoints by a google chrome screen recorder extension.

Video formats supported: `mp4, webm, avi`
## Use the API
Base local URL
```
BASE URL: http://127.0.0.1:8000/api/v1/record 
```

Deployed URL
```
BASE URL: https://recordplus.onrender.com/api/v1/record 
```

## videos

1. Upload a video


* PHASE 1: Send a video upload request with the title(optional), the description(optional) and a first chunk of your video(mandatory) . You will receive a video ID that you will use to send remaining chuncks of you video. The video ID will be in the endpoint URL

*Endpoint:*  `POST`: ```/videos/```

*Parameters:*

```
title: string, maxLength(255, optional)
description: string(optional)
video_file: binary
```

*Response:* `Code: 201`

```JSON

    {"video_id": "number"}

```

* PHASE 2: Use the received video ID to send chuncks of your video

*Endpoint:*  `PATCH`: ```/videos/{video_id}/update_video_file/```

*Parameters:*

```
video_chunk: binary
```

*Response:* `Code: 200`

```JSON
[
    {"message": "Chunk uploaded successfully"}
]
```

* PHASE 3: Keep sending the chunks and after receiving the OK response from the last chunk, send a request to finalize the upload and transcribe the video.

*Endpoint:*  `POST`: ```/videos/{video_id}/finalize_video_upload/```

*Parameters:*

```
None
```

*Response:* `Code: 200`

```JSON
[
    {"message": "Transcription task initiated"}
]
```

<!-- 1. `POST`: ```/videos/```

Upload a video

Parameters:

```
title: string, maxLength(255)
description: string
video_file: File
```

Response: `Code: 201`

```JSON
[
    {
        "id": number,
        "title": string,
        "description": string
        "video_file": string(url),
        "created_at": string(UTC time)
    },
]
``` -->

2. `GET`: ```/videos/```

Retrive all videos

Response:
`Code: 200`
```JSON
[
    {
        "id": "number",
        "title": "string",
        "description": "string"
        "video_file": "string(url)",
        "created_at": "string(UTC time)",
        "transcription:" {
            "id": "number",
            "transcription_text": "string"
        }
    },
]
```
3. `GET`: ```/videos/{video_id}/```

Retrive a video

Response:
`Code: 200`
```JSON
[
    {
        "id": "number",
        "title": "string",
        "description": "string"
        "video_file": "string(url)",
        "created_at": "string(UTC time)",
        "transcription:" {
            "id": "number",
            "transcription_text": "string"
        }
    },
]
```

4. `GET`: ```/videos/{video_id}/stream_video/```

Stream a video

Response:
`Code: 200`
```
streamed video content
```
