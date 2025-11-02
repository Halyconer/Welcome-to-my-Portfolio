# Backend Development Mode

This Flask application supports a development mode that allows testing with curl, Postman, or other HTTP clients.

## Configuration

The app uses environment variables for configuration. Copy `.env.example` to `.env` and modify as needed:

```bash
cp .env.example .env
```

## Environment Variables

- `FLASK_ENV`: Set to `development` or `production` (default: `production`)
- `DEVELOPMENT_MODE`: Set to `true` to enable development features (default: `false`)
- `BULB_IP`: IP address of your smart bulb (default: `192.168.1.210`)
- `ALLOWED_ORIGIN`: Allowed origin for production mode (default: GitHub Pages URL)

## Development Mode Features

When `DEVELOPMENT_MODE=true`:

1. **CORS**: Allows requests from any origin
2. **Authentication**: Skips origin/referer checks
3. **Debug endpoint**: `/dev/status` endpoint available for testing
4. **Verbose logging**: Shows additional debug information

## Usage Examples

### Enable Development Mode

Edit your `.env` file:
```
DEVELOPMENT_MODE=true
```

### Test with curl

```bash
# Test the brightness endpoint
curl -X POST http://localhost:5001/set_brightness \
  -H "Content-Type: application/json" \
  -d '{"brightness": 75}'

# Check development status
curl http://localhost:5001/dev/status
```

### Test with Postman

1. Set method to POST
2. URL: `http://localhost:5001/set_brightness`
3. Headers: `Content-Type: application/json`
4. Body: `{"brightness": 50}`

## Production Mode

When `DEVELOPMENT_MODE=false` (default):
- Only requests from `ALLOWED_ORIGIN` are accepted
- Origin and Referer headers are required
- `/dev/status` endpoint returns 404
- Blocks curl and Postman requests (as intended)

## Running the Application

```bash
cd backend
python app.py
```

The app will print the current configuration when it starts.
