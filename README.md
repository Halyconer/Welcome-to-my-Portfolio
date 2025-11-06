# Adrian Eddy's Portfolio

A personal portfolio website showcasing economics student Adrian Eddy's background, experience, and interactive smart light project.

## Overview

This portfolio features:

- **Interactive light control** - Visitors can adjust Adrian's NYU dorm room lights remotely
- **Professional resume** - Detailed experience in finance, data analysis, and economics
- **Clean, modern design** - Responsive web interface with smooth animations

## Features

### Smart Light Integration

- Real-time brightness control via web interface
- Flask backend controlling Yeelight smart bulbs
- Cross-origin resource sharing for secure web access
- Interactive slider with visual feedback

### Portfolio Content

- Economics student at NYU with data science focus
- Professional experience at Equitable Advisors, Henry Social, and CIMB Bank
- Leadership roles in NYU Motorsports and Data Science Club
- Skills in Python, SQL, financial analysis, and more

## Tech Stack

**Frontend:**
- HTML5, CSS3, JavaScript
- Font Awesome icons
- Google Fonts (Inter)
- Responsive CSS animations

**Backend:**
- Python Flask applications (lighting + Connect4 game)
- Yeelight Python library for smart bulb control
- Minimax algorithm with alpha-beta pruning for Connect4 AI
- SQLite database for logging interactions
- Flask-CORS for development mode
- nginx reverse proxy for production

**Infrastructure:**
- Raspberry Pi deployment
- nginx reverse proxy with CORS handling
- ngrok tunneling for secure remote access
- Environment-based configuration (development/production)

## File Structure

```
├── index.html              # Main portfolio page with interactive features
├── resume.html             # Detailed resume page  
├── dev-roadtrip.html       # Development journey page
├── styles.css              # Shared styles and animations
├── nginx.conf              # Production nginx configuration
├── assets/                 # Images and documents
│   ├── profile.jpg         # Profile photo
│   ├── connect4.jpg        # Connect4 game preview
│   ├── lightbulb_diagram.jpg # Smart home project visual
│   └── AdrianEddy.pdf # Downloadable resume
├── backend/                # Lighting control API
│   ├── app.py              # Production Flask server (port 5001)
│   ├── app_new.py          # Development version (not used in prod)
│   ├── requirements.txt    # Python dependencies
│   ├── generate_stats.py   # Analytics generation
│   └── test_app.py         # Backend tests
└── connectX/               # Connect4 game API
    ├── app.py              # Connect4 Flask server (port 5002)
    ├── Connect4.py         # Game logic
    ├── minimax.py          # AI algorithm
    ├── scoring.py          # Game evaluation
    └── requirements.txt    # Python dependencies
```

## Setup

### Frontend
1. Clone the repository
2. Open `index.html` in a web browser  
3. Navigate between pages using the navigation menu

### Backend (Optional - for smart light functionality)
1. Install Python dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
2. Configure your Yeelight bulb IP in `app.py`
3. Run the Flask server:
   ```bash
   python app.py
   ```

**For complete deployment instructions (development vs production), see [DEPLOYMENT.md](DEPLOYMENT.md)**

## Interactive Features

### Smart Light Control
The main page includes an interactive greeting system where visitors can:
- Adjust brightness using a visual slider (1-100%)
- Send their "greeting" by controlling the physical lights in Adrian's NYU dorm
- Receive real-time feedback on the light changes
- View usage statistics and analytics

### Connect4 AI Game  
An interactive Connect4 game featuring:
- Play against AI with minimax algorithm and alpha-beta pruning
- Multiple difficulty levels
- Real-time game state management
- Responsive game board with smooth animations
- Click any column to drop your piece

### Development Analytics
- Real-time usage tracking and statistics
- Database logging of all interactions
- Performance monitoring and error tracking

**For detailed API documentation and troubleshooting, see [DEPLOYMENT.md](DEPLOYMENT.md)**

## Live Demo

Visit the portfolio to experience:
- **Interactive light control** - Control real hardware from anywhere in the world
- **Connect4 AI game** - Challenge an intelligent opponent  
- **Professional portfolio** - Learn about Adrian's economics and data science background

**Current URL:** [Portfolio Website](https://halyconer.github.io/Welcome-to-my-Portfolio/)

## Contact

- **Email:** ae2422@nyu.edu
- **LinkedIn:** [adrian3ddy](https://www.linkedin.com/in/adrian3ddy/)
- **Institution:** New York University, College of Arts and Sciences

---

_Economics @ NYU · Data, Markets & Machines_
