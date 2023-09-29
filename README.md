# RecordPlus
The project is a REST API using python django to consume endpoints by a google chrome screen recorder extension.

Video formats supported: `mp4, webm, avi`
## Use the API
It is deployed at [https://recordplus.onrender.com/api/record/](https://recordplus.onrender.com/api/record/)

```
BASE URL: recordplus.onrender.com/api/
```

## videos

1. `POST`: ```/record/videos/```

Upload a video

Parameters:

```
title: string, maxLength(255)
description: string
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
```

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
