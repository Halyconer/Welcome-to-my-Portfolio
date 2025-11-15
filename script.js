// Portfolio Script
const API_BASE_URL = 'https://valid-goblin-full.ngrok-free.app'
const LIGHTING_API_URL = API_BASE_URL + '/lighting'
const CONNECT4_API_BASE = API_BASE_URL + '/connect4'

let connect4GameState = null
let isConnect4Processing = false

document.addEventListener('DOMContentLoaded', function() {
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