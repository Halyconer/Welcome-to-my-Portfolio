// Portfolio Script

// Typewriter Effect
var TxtType = function(el, toRotate, period) {
    this.toRotate = toRotate;
    this.el = el;
    this.loopNum = 0;
    this.period = parseInt(period, 10) || 2000;
    this.txt = '';
    this.tick();
    this.isDeleting = false;
};

TxtType.prototype.tick = function() {
    var i = this.loopNum % this.toRotate.length;
    var fullTxt = this.toRotate[i];

    if (this.isDeleting) {
        this.txt = fullTxt.substring(0, this.txt.length - 1);
    } else {
        this.txt = fullTxt.substring(0, this.txt.length + 1);
    }

    this.el.innerHTML = '<span class="wrap">'+this.txt+'</span>';

    var that = this;
    var delta = 80 - Math.random() * 40; // Faster typing: 40-80ms instead of 100-200ms

    if (this.isDeleting) { delta /= 2; } // Even faster deleting: 20-40ms

    if (!this.isDeleting && this.txt === fullTxt) {
        // If we're at the last text ("Welcome"), stop the animation
        if (this.loopNum === this.toRotate.length - 1) {
            // Remove the cursor after a brief pause
            setTimeout(function() {
                that.el.innerHTML = '<span class="wrap">' + that.txt + '</span>';
                that.el.querySelector('.wrap').style.borderRight = 'none';
            }, 1000);
            return; // Stop the typewriter completely
        }
        delta = this.period;
        this.isDeleting = true;
    } else if (this.isDeleting && this.txt === '') {
        this.isDeleting = false;
        this.loopNum++;
        delta = 300; // Shorter pause between words: 300ms instead of 500ms
    }

    setTimeout(function() {
        that.tick();
    }, delta);
};

// Initialize typewriter effect on window load
window.addEventListener('load', function() {
    var elements = document.getElementsByClassName('typewrite');
    for (var i=0; i<elements.length; i++) {
        var toRotate = elements[i].getAttribute('data-type');
        var period = elements[i].getAttribute('data-period');
        if (toRotate) {
            new TxtType(elements[i], JSON.parse(toRotate), period);
        }
    }
    
    // INJECT CSS for typewriter cursor
    var css = document.createElement("style");
    css.type = "text/css";
    css.innerHTML = ".typewrite > .wrap { border-right: 0.08em solid rgba(13, 59, 102, 0.7); }";
    document.body.appendChild(css);
});

const API_BASE_URL = 'https://valid-goblin-full.ngrok-free.app'
const LIGHTING_API_URL = API_BASE_URL + '/lighting'
const CONNECT4_API_BASE = API_BASE_URL + '/connect4'

let connect4GameState = null
let isConnect4Processing = false

document.addEventListener('DOMContentLoaded', function() {
    // Enhanced Navigation
    const nav = document.querySelector('.floating-nav')
    const navLinks = document.querySelectorAll('.floating-nav .nav a')
    const sections = document.querySelectorAll('section[id]')
    
    // Add scroll effect to navigation
    function handleNavScroll() {
        if (window.scrollY > 50) {
            nav.classList.add('scrolled')
        } else {
            nav.classList.remove('scrolled')
        }
    }
    
    // Highlight active section in navigation
    function updateActiveNav() {
        let current = ''
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop - 100
            const sectionHeight = section.offsetHeight
            
            if (window.scrollY >= sectionTop && window.scrollY < sectionTop + sectionHeight) {
                current = section.getAttribute('id')
            }
        })
        
        navLinks.forEach(link => {
            link.classList.remove('active')
            if (link.getAttribute('href') === '#' + current) {
                link.classList.add('active')
            }
            // Special case for home/about section
            if (current === '' && link.getAttribute('href') === 'index.html') {
                link.classList.add('active')
            }
        })
    }
    
    window.addEventListener('scroll', () => {
        handleNavScroll()
        updateActiveNav()
    })
    
    // Initialize
    handleNavScroll()
    updateActiveNav()
    
    // Create floating dots animation
    // createFloatingDots()
    
    // Cupcake popup
    initCupcakePopup()
    // Resume controls
    const openResumeBtn = document.getElementById('openResumeFullscreen')
    if (openResumeBtn) {
        openResumeBtn.addEventListener('click', () => window.open('assets/AdrianEddy.pdf', '_blank'))
    }

    // Lighting controls
    const slider = document.getElementById('brightnessSlider')
    const label = document.getElementById('brightnessValue')
    const btn = document.getElementById('setBrightnessBtn')
    const msg = document.getElementById('brightnessStatus')

    if (slider && label) {
        slider.addEventListener('input', () => label.textContent = slider.value)
    }

    if (btn && msg) {
        btn.addEventListener('click', () => {
            const brightness = slider.value
            msg.textContent = `Setting brightness to ${brightness}%...`
            btn.disabled = true
            btn.textContent = 'Sending...'

            fetch(`${LIGHTING_API_URL}/set_brightness`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'ngrok-skip-browser-warning': 'true',
                },
                body: JSON.stringify({ brightness: parseInt(brightness) }),
            })
            .then(response => {
                if (!response.ok) throw new Error(`HTTP ${response.status}: ${response.statusText}`)
                return response.json()
            })
            .then(data => {
                if (data.status === 'success') {
                    msg.textContent = `✓ Lights set to ${data.brightness_set}% — thanks for the greeting!`
                } else {
                    msg.textContent = `× ${data.error || 'Unknown error'}`
                }
            })
            .catch(err => {
                console.error('Fetch error:', err)
                if (err.message.includes('Failed to fetch') || err.message.includes('NetworkError')) {
                    msg.textContent = `× My personal high-tech self-built server is offline - please try again later`
                } else if (err.message.includes('404')) {
                    msg.textContent = `× Light control endpoint not found - I messed up the code...`
                } else if (err.message.includes('500')) {
                    msg.textContent = `× Server error - my raspberry pi is probably overloaded`
                } else {
                    msg.textContent = `× Connection failed: ${err.message}`
                }
            })
            .finally(() => {
                btn.disabled = false
                btn.textContent = 'Send Command'
            })
        })
    }

    // Smooth scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault()
            const targetElement = document.querySelector(this.getAttribute('href'))
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 20,
                    behavior: 'smooth'
                })
            }
        })
    })

    // Scroll progress bar
    const scrollProgressBar = document.getElementById('scrollProgressBar')
    window.addEventListener('scroll', function() {
        const scrollTop = window.scrollY
        const docHeight = document.documentElement.scrollHeight - window.innerHeight
        const scrollPercent = docHeight > 0 ? scrollTop / docHeight : 0
        scrollProgressBar.style.transform = `scaleY(${scrollPercent})`
    })
})

// Connect4 functions
function showConnect4Game() {
    document.getElementById('connect4Modal').style.display = 'flex'
}

function closeConnect4Game() {
    document.getElementById('connect4Modal').style.display = 'none'
}

function newConnect4Game() {
    startConnect4Game()
}

function createConnect4Board() {
    const board = document.getElementById('connect4Board')
    board.innerHTML = ''
    
    for (let row = 5; row >= 0; row--) {
        for (let col = 0; col < 7; col++) {
            const cell = document.createElement('div')
            cell.className = 'connect4-cell'
            cell.dataset.row = row
            cell.dataset.col = col
            cell.onclick = () => makeConnect4Move(col)
            board.appendChild(cell)
        }
    }
}

function updateConnect4Board() {
    if (!connect4GameState) return
    
    const cells = document.querySelectorAll('.connect4-cell')
    cells.forEach(cell => {
        cell.className = 'connect4-cell'
        const row = parseInt(cell.dataset.row)
        const col = parseInt(cell.dataset.col)
        const piece = connect4GameState.board[row][col]
        
        if (piece === 1) cell.classList.add('player1')
        if (piece === 2) cell.classList.add('player2')
    })
}

function updateConnect4Status(message) {
    document.getElementById('connect4Status').textContent = message
}

async function connect4ApiRequest(endpoint, method = 'GET', data = null) {
    try {
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json',
                'ngrok-skip-browser-warning': 'true',
            }
        }
        
        if (data) options.body = JSON.stringify(data)
        
        const response = await fetch(CONNECT4_API_BASE + endpoint, options)
        
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`)
        
        return await response.json()
    } catch (error) {
        console.error('Connect4 API request failed:', error)
        updateConnect4Status('Connection error! Make sure the game server is running on your Pi.')
        return null
    }
}

async function startConnect4Game() {
    isConnect4Processing = true
    updateConnect4Status('Starting new game...')
    
    const response = await connect4ApiRequest('/play', 'POST')
    console.log('New Connect4 game response:', response)
    
    if (response) {
        connect4GameState = response
        createConnect4Board()
        updateConnect4Board()
        updateConnect4Status('Your turn! Click a column to drop your piece.')
    } else {
        updateConnect4Status('Failed to start new game. Check server connection.')
    }
    
    isConnect4Processing = false
}

async function makeConnect4Move(col) {
    console.log('Connect4 move called with column:', col)
    
    if (isConnect4Processing || !connect4GameState || connect4GameState.game_over) {
        console.log('Move blocked - processing:', isConnect4Processing, 'gameState exists:', !!connect4GameState)
        return
    }
    
    const validCols = connect4GameState.valid_cols || []
    console.log('Valid columns:', validCols, 'Clicked:', col)
    
    if (!validCols.includes(col)) {
        updateConnect4Status('Invalid move! Column is full.')
        return
    }
    
    isConnect4Processing = true
    updateConnect4Status('Processing move...')
    
    const response = await connect4ApiRequest('/move', 'POST', { column: col })
    
    if (response) {
        if (response.game_over) {
            connect4GameState = { ...response, board: response.board_after_ai || response.board }
            updateConnect4Board()
            
            if (response.winner === 'player') {
                updateConnect4Status('🎉 You won! Great job!')
            } else if (response.winner === 'ai') {
                updateConnect4Status('🤖 AI wins! Try again?')
            } else if (response.winner === 'tie') {
                updateConnect4Status('🤝 It\'s a tie! Well played!')
            } else {
                updateConnect4Status('Game over!')
            }
        } else {
            connect4GameState = { ...response, board: response.board_before_ai }
            updateConnect4Board()
            updateConnect4Status('Your move made! AI is thinking...')
            
            setTimeout(() => {
                connect4GameState = { ...response, board: response.board_after_ai }
                updateConnect4Board()
                
                if (response.ai_move !== null && response.ai_move !== undefined) {
                    updateConnect4Status(`AI dropped in column ${response.ai_move + 1}. Your turn!`)
                } else {
                    updateConnect4Status('Your turn! Click a column to drop your piece.')
                }
            }, 1000)
        }
    }
    
    isConnect4Processing = false
}

// Close modal when clicking outside
window.addEventListener('click', function(event) {
    const modal = document.getElementById('connect4Modal')
    if (event.target === modal) closeConnect4Game()
})

// Chart Line Animation
function createFloatingDots() {
    const heroBackground = document.querySelector('.hero-background')
    if (!heroBackground) return
    
    createAnimatedChart()
}

function createAnimatedChart() {
    const heroBackground = document.querySelector('.hero-background')
    const heroSection = document.querySelector('.hero')
    
    // Create canvas covering the entire hero section
    const canvas = document.createElement('canvas')
    canvas.className = 'chart-line'
    
    const rect = heroSection.getBoundingClientRect()
    canvas.width = rect.width
    canvas.height = rect.height
    
    canvas.style.cssText = `
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        opacity: 0.15;
        pointer-events: none;
    `
    
    heroBackground.appendChild(canvas)
    animateChartLine(canvas)
}

function animateChartLine(canvas) {
    const ctx = canvas.getContext('2d')
    const width = canvas.width
    const height = canvas.height
    
    // Generate chart data points
    const totalPoints = 100
    const chartData = []
    let currentY = height * 0.7 // Start at 70% down the screen
    
    for (let i = 0; i < totalPoints; i++) {
        const x = (i / (totalPoints - 1)) * width
        // Random walk with slight upward trend
        const change = (Math.random() - 0.4) * 30
        currentY += change
        currentY = Math.max(height * 0.3, Math.min(height * 0.8, currentY))
        
        chartData.push({ x, y: currentY })
    }
    
    // Animation state
    let currentPoint = 0
    const totalDuration = 5500 // 5.5 seconds to match "nice to meet you" completion
    const pointsPerFrame = totalPoints / (totalDuration / 16) // 60fps
    
    function drawLine() {
        ctx.clearRect(0, 0, width, height)
        
        if (currentPoint < totalPoints) {
            // Create gradient for the line
            const gradient = ctx.createLinearGradient(0, 0, width, 0)
            gradient.addColorStop(0, '#4a90e2')
            gradient.addColorStop(0.5, '#3a7ca5')
            gradient.addColorStop(1, '#0d3b66')
            
            // Draw the line up to current point
            ctx.strokeStyle = gradient
            ctx.lineWidth = 3
            ctx.lineCap = 'round'
            ctx.lineJoin = 'round'
            ctx.beginPath()
            
            for (let i = 0; i <= Math.floor(currentPoint); i++) {
                const point = chartData[i]
                if (i === 0) {
                    ctx.moveTo(point.x, point.y)
                } else {
                    ctx.lineTo(point.x, point.y)
                }
            }
            ctx.stroke()
            
            // Draw current point with glow effect
            const currentData = chartData[Math.floor(currentPoint)]
            if (currentData) {
                // Glow effect
                ctx.shadowColor = '#4a90e2'
                ctx.shadowBlur = 10
                ctx.fillStyle = '#4a90e2'
                ctx.beginPath()
                ctx.arc(currentData.x, currentData.y, 4, 0, Math.PI * 2)
                ctx.fill()
                ctx.shadowBlur = 0
            }
            
            // Increment current point
            currentPoint += pointsPerFrame
            
            // Continue animation
            requestAnimationFrame(drawLine)
        }
    }
    
    // Start animation after a short delay
    setTimeout(() => {
        drawLine()
    }, 500)
}

// Cupcake popup functionality
function initCupcakePopup() {
    // Always show the cupcake popup
    
    // Create popup HTML as bottom bar
    const popup = document.createElement('div')
    popup.className = 'cupcake-bar'
    popup.innerHTML = `
        <div class="cupcake-bar-content">
            <div class="cupcake-message">
                <span class="cupcake-text">This website uses chocolate to ensure you get the best experience on our website.</span>
            </div>
            <div class="cupcake-buttons">
                <button class="cupcake-accept">Accept Chocolate</button>
                <button class="cupcake-decline">Decline</button>
            </div>
        </div>
    `
    
    document.body.appendChild(popup)
    
    // Show popup immediately
    setTimeout(() => {
        popup.classList.add('show')
    }, 1000)
    
    // Handle button clicks
    popup.querySelector('.cupcake-accept').addEventListener('click', () => {
        popup.classList.add('hide')
        setTimeout(() => popup.remove(), 400)
        createFallingChocolate()
        showPlusOneButton()
    })
    
    popup.querySelector('.cupcake-decline').addEventListener('click', () => {
        popup.classList.add('hide')
        setTimeout(() => popup.remove(), 400)
    })
}

function createFallingChocolate() {
    const chocolate = document.createElement('div')
    chocolate.className = 'falling-chocolate'
    chocolate.textContent = '🍫'
    
    // Random horizontal position
    chocolate.style.left = Math.random() * (window.innerWidth - 60) + 'px'
    
    document.body.appendChild(chocolate)
    
    // Remove after animation
    setTimeout(() => {
        if (chocolate.parentNode) {
            chocolate.remove()
        }
    }, 3000)
}

function showPlusOneButton() {
    const plusOneBtn = document.createElement('div')
    plusOneBtn.className = 'plus-one-chocolate'
    plusOneBtn.innerHTML = '+1 🍫'
    
    // Position to the right side
    plusOneBtn.style.right = '30px'
    plusOneBtn.style.top = '50%'
    
    document.body.appendChild(plusOneBtn)
    
    // Remove after animation
    setTimeout(() => {
        if (plusOneBtn.parentNode) {
            plusOneBtn.remove()
        }
    }, 2000)
}