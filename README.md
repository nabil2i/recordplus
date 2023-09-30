# RecordPlus
The project is a REST API using python django to consume endpoints by a google chrome screen recorder extension.

Video formats supported: `mp4, webm, avi`
## Use the API
It is deployed at [https://recordplus.onrender.com/api/record/](https://recordplus.onrender.com/api/record/)

```
BASE URL: recordplus.onrender.com/api/
```

## videos

1. 

    Upload a video

* PHASE 1: Send a video upload request with the title and the description. You will receive a video ID that will we use to send chuncks of video

*Endpoint:*  `POST`: ```/record/videos/```

*Parameters:*

```
title: string, maxLength(255)
description: string
```

*Response:* `Code: 201`

```JSON
[
    {"video_id": number}
]
```

* PHASE 2: Use the received video ID to send chuncks of your video

*Endpoint:*  `PATCH`: ```/record/videos/update_video_chunck```

*Parameters:*

```
video_id: string
video_chunck: binary
```

*Response:* `Code: 200`

```JSON
[
    {'message': 'Chunk uploaded successfully'}
]
```

* PHASE 3: Keep sending the chunks and after receiving the OK response from the last chunk, send a request to finalize the upload and transcribe the video.

*Endpoint:*  `POST`: ```/record/videos/finalize_video_upload```

*Parameters:*

```
video_id: string
```

*Response:* `Code: 200`

```JSON
[
    {'message': 'Transcription task initiated'}
]
```

<!-- 1. `POST`: ```/record/videos/```

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

2. `GET`: ```/record/videos/```

Retrive all videos

Response:
`Code: 200`
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
```
3. `GET`: ```/record/videos/{id}```

Retrive a video

Response:
`Code: 200`
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
```

4. `GET`: ```/record/videos/{id}/stream_video/```

Stream a video

Response:
`Code: 200`
```
streamed video content
```
