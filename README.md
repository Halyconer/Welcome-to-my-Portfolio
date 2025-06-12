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

- Python Flask application
- Yeelight Python library for smart bulb control
- Flask-CORS for cross-origin requests
- JSON API endpoints

## File Structure

```
├── index.html          # Main portfolio page with interactive light control
├── resume.html         # Detailed resume page
├── styles.css          # Shared styles and animations
├── assets/
│   ├── profile.jpg     # Profile photo
│   └── Adrian_Eddy_Resume.pdf  # Downloadable resume
└── backend/
    ├── app.py          # Flask server for light control
    ├── requirements.txt # Python dependencies
    └── test_app.py     # Backend tests
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

## Interactive Features

The main page includes an interactive greeting system where visitors can:

- Adjust brightness using a visual slider (1-100%)
- Send their "greeting" by controlling the physical lights
- Receive real-time feedback on the light changes

This creates a unique, personal connection between the visitor and Adrian's physical space at NYU.

## Live Demo

Visit the portfolio to experience the interactive light control and learn more about Adrian's background in economics, data science, and financial markets.

## Contact

- **Email:** ae2422@nyu.edu
- **LinkedIn:** [adrian3ddy](https://www.linkedin.com/in/adrian3ddy/)
- **Institution:** New York University, College of Arts and Sciences

---

_Economics @ NYU · Data, Markets & Machines_
