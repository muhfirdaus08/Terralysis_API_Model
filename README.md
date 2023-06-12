# API Model Documentation

![banner.](/banner1.png)

##### base url : `https://<cloudrun_service_name>.a.run.app/`

##### live demo : `https://<cloudrun_service_name>.a.run.app/docs`

##### base image url : `https://storage.googleapis.com/<bucket_name>/<image_name.jpg>`

![endpoint.](/endpoint.png)

### - Read Root

- Path :
  - `/`
- Method:
  - `GET`
- Response
  ```
  {
    "Status": "Ok"
  }
  ```

### - Upload an Image as User

- Path :
  - `/analysis`
- Method:
  - `POST`
- Header
  - `Authorization: Bearer <token>`
- Request
  - `userId as string`
  - `image as file, key: file`
- Response
  ```
  {
    "message": "Image User Upload Successfully and Get Prediction",
    "imageId": "deb791e4-9858-4982-9485-c9291b4ac0f7",
    "url": "https://storage.googleapis.com/<bucket_name>/<image_name.jpg>",
    "kelas": "Clay: 99.36%"
  }
  ```

### - Get All Image User

- Path :
  - `/analysis/{userId}`
- Method:
  - `GET`
- Header
  - `Authorization: Bearer <token>`
- Request Parameter
  - `userId as string`
- Response
  ```
  {
    "status_code": 200,
    "message": "Get All Images User Success",
    "image": [
        {
            "imageId": "004a6f8a-d185-4b0c-a8ea-90e79f670efe",
            "url": "https://storage.googleapis.com/<bucket_name>/<image_name.jpg>",
            "kelas": "Clay: 93.02%",
            "createdAt": "2023-06-12T09:55:12"
        },
        {
            "imageId": "15c284df-ef0b-473f-87fb-672d6c11ca71",
            "url": "hhttps://storage.googleapis.com/<bucket_name>/<image_name.jpg>",
            "kelas": "Red: 99.99%",
            "createdAt": "2023-06-12T11:16:11"
        },
        {
            "imageId": "deb791e4-9858-4982-9485-c9291b4ac0f7",
            "url": "https://storage.googleapis.com/<bucket_name>/<image_name.jpg>",
            "kelas": "Clay: 99.36%",
            "createdAt": "2023-06-12T16:51:25"
        }
     ]
  }
  ```

### - Get Detail Image User

- Path :
  - `/analysis/{userId}/{imageId}`
- Method:
  - `GET`
- Header
  - `Authorization: Bearer <token>`
- Request Parameter
  - `userId as string`
  - `imageId as string`
- Response
  ```
  {
    "status_code": 200,
    "message": "Get Detail Image User Success",
    "image": {
        "url": "https://storage.googleapis.com/<bucket_name>/<image_name.jpg>",
        "mimetype": "image/jpeg",
        "userId": "3df3261b-1662-4199-a88b-9d7c9f2b7941",
        "kelas": "Red: 99.99%",
        "long_desc": long desc,
        "persebaran": persebaran,
        "ciri_fisik": ciri fisik,
        "ciri_morfologi": ciri morfologi,
        "updatedAt": "2023-06-12T11:16:11",
        "imageId": "15c284df-ef0b-473f-87fb-672d6c11ca71",
        "originalname": "Red_32.jpg",
        "size": 38561,
        "short_desc": short desc,
        "kandungan": kandungan,
        "ciri_kimia": ciri kimia,
        "createdAt": "2023-06-12T11:16:11"
    }
  }
  ```

### - Delete an Image User

- Path :
  - `/analysis/{userId}/{imageId}`
- Method:
  - `DELETE`
- Header
  - `Authorization: Bearer <token>`
- Request Parameter
  - `userId as string`
  - `imageId as string`
- Response
  ```
  {
    "status_code": 200,
    "message": "Delete Image Success"
  }
  ```

### - Upload an Image as Guest

- Path :
  - `/analysis-guest`
- Method:
  - `POST`
- Request
  - `image as file, key: file`
- Response
  ```
  {
    "message": "Image Guest Upload Successfully and Get Prediction",
    "imageGuestId": "8cb7f57b-3d61-45e4-97e4-3b4d84e35416",
    "url": "https://storage.googleapis.com/<bucket_name>/<image_name.jpg>",
    "kelas": "Clay: 99.36%"
  }
  ```

### - Get Detail Image Guest

- Path :
  - `/analysis-guest/{image_guestId}`
- Method:
  - `GET`
- Request Parameter
  - `image_guestId as string`
- Response
  ```
  {
    "status_code": 200,
    "message": "Get Detail Image Guest Success",
    "image": {
        "url": "https://storage.googleapis.com/<bucket_name>/<image_name.jpg>",
        "mimetype": "image/jpeg",
        "userId": "3df3261b-1662-4199-a88b-9d7c9f2b7941",
        "kelas": "Red: 99.99%",
        "long_desc": long desc,
        "persebaran": persebaran,
        "ciri_fisik": ciri fisik,
        "ciri_morfologi": ciri morfologi,
        "updatedAt": "2023-06-12T11:16:11",
        "imageGuestId": "15c284df-ef0b-473f-87fb-672d6c11ca71",
        "originalname": "Red_32.jpg",
        "size": 38561,
        "short_desc": short desc,
        "kandungan": kandungan,
        "ciri_kimia": ciri kimia,
        "createdAt": "2023-06-12T11:16:11"
    }
  }
  ```
