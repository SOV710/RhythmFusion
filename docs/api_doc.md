# API DOC

## user

| Endpoint                | Description |
| ----------------------- | ----------- |
| GET /api/user/profile   | Profile     |
| POST /api/user/login    | Login       |
| POST /api/user/register | Register    |
| POST /api/user/logout   | Logout      |

## music

| Endpoint                          | Description               |
| --------------------------------- | ------------------------- |
| GET /api/music/?search={keyword}/ | Search songs              |
| POST /api/music/csv/              | Import CSV songs          |
| GET /api/music/genres/{code}/     | Recommend based on genres |


## playlist


| Endpoint                                          | Description                    |
| ------------------------------------------------- | ------------------------------ |
| POST /api/playlists/                              | Create Playlists               |
| GET /api/playlists/{id}/                          | Get one playlist               |
| GET /api/playlists/{id}/tracks/                   | List tracks in playlist        |
| POST /api/playlists/{id}/tracks/                  | Add track                      |
| DELETE /api/playlists/{id}/tracks/{song_id}/      | Remove track                   |
| GET /api/playlists/{playlist_id}/recommendations/ | Recommend songs for a playlist |
