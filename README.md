# RecordPlus
The project is a REST API using pythondjango to consume endpoints by a google chrome screen recorder extension.

## Use the API
It is deployed at [https://recordplus.onrender.com/api/](https://recordplus.onrender.com/api/)

```
BASE URL: recordplus.onrender.com/api/
```

## videos

1. `POST`: ```/videos/```

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

2. `GET`: ```/videos/```

Retrive all videos

Response:
`Code: 200`
```JSON
[
    {
        "id": number,
        "title": string,
        "description": string
        "video_file": string,
        "created_at": string(UTC time)
    },
]
```
3. `GET`: ```/videos/{id}```

Retrive a video

Response:
`Code: 200`
```JSON
[
    {
        "id": number,
        "title": string,
        "description": string
        "video_file": string,
        "created_at": string(UTC time)
    },
]
```

4. `GET`: ```/videos/{id}/stream_video/```

Stream a video

Response:
`Code: 200`
```
streamed video content
```