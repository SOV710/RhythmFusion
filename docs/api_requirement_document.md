# API List

1. Search api
2. Suggest api
3. User Profile api
4. I18n api (optional)
5. Playlist api
6. Suggest api (based on genres)
7. CSV Post api

# API Name: Search API

## 1. Endpoint
POST /api/music/

## 2. Method
GET

### Sample Request Body
```json
{
  "username": "Spallanzani",
  "avatar": "https://cdn.example.com/avatar.jpg"
}
```

# API Name: Update User Profile

## 1. Endpoint
POST /api/profile

## 2. Method
POST

## 3. Request Parameters

| Parameter  | Type    | Required | Description             |
|------------|---------|----------|-------------------------|
| username   | string  | Yes      | The new username        |
| avatar     | string  | No       | URL of the avatar image |

### Sample Request Body
```json
{
  "username": "Spallanzani",
  "avatar": "https://cdn.example.com/avatar.jpg"
}
