#!/bin/bash

# Local Testing Script
# Run this on your development machine to test the setup

echo "🧪 Testing Portfolio Setup Locally..."

# Check if required files exist
echo "📋 Checking files..."
if [ ! -f "nginx.conf" ]; then
    echo "❌ nginx.conf not found"
    exit 1
fi

if [ ! -f "backend/app.py" ]; then
    echo "❌ backend/app.py not found"
    exit 1
fi

if [ ! -f "connectX/app.py" ]; then
    echo "❌ connectX/app.py not found"
    exit 1
fi

echo "✅ All required files found"

# Test nginx config syntax (if nginx is installed)
if command -v nginx &> /dev/null; then
    echo "🔧 Testing nginx configuration..."
    nginx -t -c $(pwd)/nginx.conf
    if [ $? -eq 0 ]; then
        echo "✅ Nginx configuration is valid"
    else
        echo "❌ Nginx configuration error"
        exit 1
    fi
else
    echo "⚠️ nginx not installed - skipping config test"
fi

# Check Python dependencies
echo "🐍 Checking Python dependencies..."

cd backend
if [ ! -d "venv" ]; then
    echo "📦 Creating backend virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt
echo "✅ Backend dependencies OK"
deactivate
cd ..

cd connectX
if [ ! -d ".venv" ]; then
    echo "📦 Creating Connect4 virtual environment..."
    python3 -m venv .venv
fi

source .venv/bin/activate
pip install flask flask-cors numpy pandas scipy
echo "✅ Connect4 dependencies OK"
deactivate
cd ..

# Test Flask apps startup
echo "🚀 Testing Flask apps..."

# Test backend
cd backend
source venv/bin/activate
timeout 5s python app.py &
BACKEND_PID=$!
sleep 2
if kill -0 $BACKEND_PID 2>/dev/null; then
    echo "✅ Backend Flask app starts successfully"
    kill $BACKEND_PID
else
    echo "❌ Backend Flask app failed to start"
fi
deactivate
cd ..

# Test Connect4
cd connectX
source .venv/bin/activate
timeout 5s python app.py &
CONNECT4_PID=$!
sleep 2
if kill -0 $CONNECT4_PID 2>/dev/null; then
    echo "✅ Connect4 Flask app starts successfully"
    kill $CONNECT4_PID
else
    echo "❌ Connect4 Flask app failed to start"
fi
deactivate
cd ..

echo ""
echo "🎉 Local testing complete!"
echo "📋 Summary:"
echo "   ✅ Configuration files valid"
echo "   ✅ Dependencies installed"
echo "   ✅ Flask apps start successfully"
echo ""
echo "🚀 Ready to deploy to Raspberry Pi!"
echo "📝 Next steps:"
echo "   1. Transfer files to Pi: scp -r . pi@your-pi-ip:/home/pi/portfolio"
echo "   2. Run setup.sh on Pi"
echo "   3. Start ngrok: ngrok http 8080"
echo "   4. Update API_BASE_URL in HTML"
echo "   5. Deploy to GitHub Pages"
