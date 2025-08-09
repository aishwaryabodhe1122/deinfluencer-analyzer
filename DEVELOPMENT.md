# Development Guide

## Quick Start

### Option 1: Using the Batch Script (Recommended)
Simply double-click `start-dev.bat` to start both servers automatically.

### Option 2: Manual Setup

1. **Start Backend Server:**
   ```bash
   cd backend
   python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Start Frontend Server (in a new terminal):**
   ```bash
   cd frontend
   npm run dev
   ```

## Access Points

- **Frontend Application:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs
- **API Health Check:** http://localhost:8000/health

## Testing the Application

1. Open http://localhost:3000 in your browser
2. Enter a username (try "johndoe" or "janesmith" for demo data)
3. Select a platform (Instagram, Twitter, etc.)
4. Click "Analyze" to see the authenticity score

## Demo Usernames

The application includes mock data for these usernames:
- `johndoe` - High follower count, verified account
- `janesmith` - Moderate follower count, authentic content creator
- Any other username will generate random demo data

## Project Structure

```
deinfluencer-analyzer/
├── frontend/                 # Next.js React application
│   ├── src/
│   │   ├── app/             # App router pages
│   │   └── components/      # React components
│   ├── package.json
│   └── Dockerfile.dev
├── backend/                  # FastAPI Python application
│   ├── main.py             # Main application file
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile.dev
├── docker-compose.yml       # Docker setup
├── start-dev.bat           # Development startup script
└── README.md               # Project documentation
```

## Key Features

### Frontend Components
- **Navbar:** Navigation with branding
- **SearchSection:** Hero section with influencer search
- **AnalysisResults:** Comprehensive authenticity score display
- **TrendingInfluencers:** Trending authentic influencers
- **Footer:** Professional footer with links

### Backend API Endpoints
- `POST /api/analyze` - Analyze influencer authenticity
- `GET /api/trending` - Get trending influencers
- `GET /health` - Health check endpoint
- `GET /docs` - Interactive API documentation

### Authenticity Scoring
- **Overall Score:** Composite authenticity rating (0-10)
- **Engagement Quality:** Analysis of engagement patterns
- **Content Authenticity:** Content quality assessment
- **Follower Authenticity:** Fake follower detection
- **Sponsored Ratio:** Balance of organic vs sponsored content
- **Consistency Score:** Posting pattern analysis

## Next Steps for Development

1. **Real Social Media Integration:**
   - Instagram Basic Display API
   - Twitter API v2
   - TikTok API
   - YouTube Data API

2. **AI/ML Enhancement:**
   - Replace mock scoring with real ML models
   - Natural language processing for content analysis
   - Computer vision for image authenticity
   - Engagement pattern detection algorithms

3. **Database Integration:**
   - User authentication system
   - Analysis history storage
   - Influencer profile caching
   - Real-time data updates

4. **Advanced Features:**
   - User accounts and watchlists
   - Email alerts for score changes
   - Comparative analysis tools
   - Export and reporting features

## Troubleshooting

### Backend Issues
- Ensure Python 3.9+ is installed
- Check that port 8000 is available
- Verify all dependencies are installed

### Frontend Issues
- Ensure Node.js 18+ is installed
- Check that port 3000 is available
- Run `npm install` if dependencies are missing

### CORS Issues
- Backend is configured to allow localhost:3000
- Check that both servers are running on correct ports
