# RhythmFusion System Architecture

This document provides a comprehensive overview of the RhythmFusion music recommendation system's architecture, covering both high-level system design and detailed component interactions.

## System Overview

RhythmFusion is built as a modern web application with a clear separation between frontend and backend components. The architecture follows industry best practices for scalability, maintainability, and performance.

```mermaid
graph TD
    User[User] -->|Interacts with| Frontend[Vue.js Frontend]
    Frontend -->|API Requests| Backend[Django Backend]
    Backend -->|Returns Data| Frontend
    Backend -->|Reads/Writes| Database[(Database)]
    Backend -->|Processes Music Data| RecommendationEngine[Recommendation Engine]
    RecommendationEngine -->|Generates Recommendations| Database
```

## Architectural Principles

RhythmFusion's architecture is guided by the following principles:

1. **Separation of Concerns**: Clear boundaries between frontend, backend, and recommendation systems
2. **RESTful Design**: Standardized API design following REST principles
3. **Component-Based UI**: Modular, reusable UI components
4. **Reactive State Management**: Centralized, reactive state management
5. **Hybrid Recommendation Strategy**: Combining collaborative filtering with content-based approaches
6. **Scalable Data Processing**: Efficient processing of music metadata and user interactions

## Frontend Architecture

The frontend is built with Vue.js 3, utilizing the Composition API and TypeScript for maintainable, type-safe code.

### Frontend Component Hierarchy

```mermaid
graph TD
    App[App.vue] --> Router[Vue Router]
    Router --> Pages[Page Components]
    Pages --> BaseComponents[Base Components]
    Pages --> BusinessComponents[Business Components]
  
    subgraph Page Components
        Home[Home.vue]
        Music[Music.vue]
        Playlist[Playlist.vue]
        UserProfile[Profile.vue]
    end
  
    subgraph Base Components
        BaseHeader[BaseHeader.vue]
        BaseMain[BaseMain.vue]
        BaseFooter[BaseFooter.vue]
    end
  
    subgraph Business Components
        MusicCard[MusicCard.vue]
        PlaylistCard[PlaylistCard.vue]
        PlayerControls[PlayerControls.vue]
    end
```

### Frontend Directories Structure

```
frontend/
├── src/
│   ├── api/              # API client and modules
│   │   ├── client.ts     # Base Axios configuration
│   │   ├── modules/      # API modules by feature
│   │   └── types.d.ts    # API type definitions
│   ├── assets/           # Static assets
│   ├── components/       # Vue components
│   │   ├── base/         # Base UI components
│   │   └── business/     # Business-specific components
│   ├── composables/      # Reusable composition functions
│   ├── pages/            # Page components
│   ├── router/           # Vue Router configuration
│   ├── stores/           # Pinia state stores
│   ├── styles/           # Global SCSS styles
│   └── types/            # TypeScript type definitions
```

### State Management

State management is implemented using Pinia, the official Vue state management library. Stores are organized by domain:

```mermaid
graph LR
  %% 定义子图
  subgraph "Pinia Stores"
    US[User Store]
    PS[Playlist Store]
    MS[Music Store]
  end

  subgraph Components
    C[Components]
  end

  subgraph API
    A[API Modules]
  end

  %% 组件与各 Store 的读写关系
  C <-->|Read/Write| US
  C <-->|Read/Write| PS
  C <-->|Read/Write| MS

  %% 各 Store 与 API 的调用关系
  US -->|API Calls| A
  PS -->|API Calls| A
  MS -->|API Calls| A

```

## Backend Architecture

The backend is built with Django and Django REST Framework, structured as a collection of apps each handling specific business domains.

### Backend Modules

```mermaid
graph TD
    Django --> User[User App]
    Django --> Music[Music App]
    Django --> Playlist[Playlist App]
    Django --> Recommender[Recommendation App]
  
    User --> Auth[Authentication]
    User --> Profiles[User Profiles]
  
    Music --> Songs[Song Management]
    Music --> Metadata[Metadata Processing]
  
    Playlist --> Creator[Playlist Creation]
    Playlist --> Management[Playlist Management]
  
    Recommender --> CF[Collaborative Filtering]
    Recommender --> Content[Content Analysis]
    Recommender --> Hybrid[Hybrid Recommender]
```

### Database Schema Design

The core data model establishes relationships between users, songs, playlists, and user interactions:

```mermaid
erDiagram
    User ||--o{ UserProfile : has
    User ||--o{ Playlist : creates
    User ||--o{ UserInteraction : generates
  
    Playlist ||--o{ PlaylistTrack : contains
    PlaylistTrack }o--|| Song : references
  
    Song }o--|| Genre : belongs_to
    Song }o--|| Artist : performed_by
  
    UserInteraction }o--|| Song : with
    UserInteraction {
        string type
        datetime timestamp
        float rating
    }
```

## Recommendation System Architecture

The recommendation system is a key component of RhythmFusion, providing personalized music recommendations through a hybrid approach.

### Recommendation Workflow

```mermaid
graph TD
    UserData[User Interaction Data] --> Preprocessing[Data Preprocessing]
    MusicMetadata[Music Metadata] --> Preprocessing
  
    Preprocessing --> CF[Collaborative Filtering]
    Preprocessing --> ContentAnalysis[Content Analysis]
  
    CF --> UserVectors[User Vectors]
    CF --> ItemVectors[Item Vectors]
    ContentAnalysis --> ContentVectors[Content Vectors]
  
    UserVectors --> HybridModel[Hybrid Model]
    ItemVectors --> HybridModel
    ContentVectors --> HybridModel
  
    HybridModel --> IndexBuilder[FAISS Index Builder]
    IndexBuilder --> VectorIndex[Vector Index]
  
    UserProfile[User Profile] --> QueryGenerator[Query Generator]
    QueryGenerator --> VectorSearch[Vector Search]
    VectorSearch --> VectorIndex
    VectorSearch --> SortedResults[Sorted Results]
    SortedResults --> FinalRecommendations[Final Recommendations]
```

### Recommendation Algorithms

The system uses multiple algorithms working together:

1. **Collaborative Filtering**: Using Singular Value Decomposition (SVD) to identify patterns in user-item interactions
2. **Content-Based Analysis**: Extracting features from music metadata (genres, artists, acoustic features)
3. **Hybrid Approach**: Combining both methods with weighted vectors
4. **Fast Similarity Search**: Using FAISS for efficient nearest-neighbor search in high-dimensional spaces

## API Architecture

The API follows RESTful design principles and is secured with JWT authentication.

### API Endpoints Structure

```mermaid
graph TD
    API[API Root] --> Auth[Authentication]
    API --> UserAPI[User API]
    API --> MusicAPI[Music API]
    API --> PlaylistAPI[Playlist API]
    API --> RecommendationAPI[Recommendation API]
  
    Auth --> Register["/api/user/register"]
    Auth --> Login["/api/user/login"]
    Auth --> Refresh["/api/user/refresh"]
  
    UserAPI --> Profile["/api/user/profile"]
    UserAPI --> LikedSongs["/api/user/liked-songs"]
  
    MusicAPI --> Songs["/api/music/songs"]
    MusicAPI --> Search["/api/music/search"]
  
    PlaylistAPI --> List["/api/playlist"]
    PlaylistAPI --> Detail["/api/playlist/{id}"]
    PlaylistAPI --> Tracks["/api/playlist/{id}/tracks"]
  
    RecommendationAPI --> ForUser["/api/recommendation/for-user"]
    RecommendationAPI --> BySong["/api/recommendation/by-song/{id}"]
    RecommendationAPI --> ByGenre["/api/recommendation/by-genre/{id}"]

```

## Request Flow

The following diagram illustrates the flow of a typical request through the system:

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant APIClient
    participant Backend
    participant Database
    participant RecommendationEngine
  
    User->>Frontend: Interacts with UI
    Frontend->>APIClient: Makes API request
    APIClient->>Backend: HTTP request with JWT
    Backend->>Backend: Validates JWT
    Backend->>Database: Queries data
  
    alt Recommendation Request
        Backend->>RecommendationEngine: Request recommendations
        RecommendationEngine->>Database: Fetch user history
        RecommendationEngine->>RecommendationEngine: Process recommendation
        RecommendationEngine-->>Backend: Return recommendations
    end
  
    Backend-->>APIClient: JSON response
    APIClient-->>Frontend: Parsed data
    Frontend->>Frontend: Update UI state
    Frontend-->>User: Updated UI
```

## Deployment Architecture

RhythmFusion supports multiple deployment configurations:

### Development Environment

```mermaid
graph TD
    DevFrontend[Vue Dev Server] -->|API Calls| DevBackend[Django Dev Server]
    DevBackend -->|Read/Write| DevDB[(SQLite Database)]
```

### Production Environment

```mermaid
graph TD
    Client[Web Browser] -->|HTTPS| WebServer[Nginx Web Server]
    WebServer -->|Static Files| StaticFiles[Static Files]
    WebServer -->|API Requests| AppServer[Gunicorn App Server]
    AppServer -->|WSGI| Django[Django Application]
    Django -->|ORM| Database[(MySQL Database)]
    Django --> Cache[(Redis Cache)]
```

## Security Architecture

Security is built into each layer of the application:

1. **Frontend Security**:

   - CSRF protection
   - Content Security Policy
   - Input validation
2. **API Security**:

   - JWT authentication
   - Permission-based access control
   - Rate limiting
3. **Backend Security**:

   - Password hashing with bcrypt
   - Database query parameterization
   - Sensitive data encryption
4. **Infrastructure Security**:

   - HTTPS/TLS encryption
   - Firewall rules
   - Regular security updates

## Performance Considerations

The architecture is designed for optimal performance through:

1. **Frontend Optimizations**:

   - Code splitting and lazy loading
   - Asset optimization
   - Client-side caching
2. **Backend Optimizations**:

   - Database query optimization
   - Response caching
   - Asynchronous task processing
3. **Recommendation System Optimizations**:

   - Efficient vector operations
   - Indexed similarity search
   - Background model updates

## Conclusion

RhythmFusion's architecture is designed to provide a robust, scalable platform for music recommendation. The separation of concerns, modular design, and focus on performance create a system that delivers personalized music experiences while remaining maintainable and extensible.

The hybrid recommendation approach balances the strengths of collaborative filtering and content-based analysis, providing recommendations that combine user preference patterns with music content characteristics.

For more detailed information on specific components, please refer to the relevant documentation sections:

- [Frontend Documentation](frontend/index.md)
- [Backend Documentation](backend/index.md)
- [Recommendation System](backend/recommendation.md)
- [API Documentation](api_doc.md)
