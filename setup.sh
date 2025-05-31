# MovieObserver Setup Script

# Create virtual environment if it doesn't exist
if [ ! -d "./movieobserver-env" ]; then
    echo "Creating virtual environment..."
    python3 -m venv movieobserver-env
fi

# Activate virtual environment
echo "Activating virtual environment..."
source movieobserver-env/bin/activate

# Install backend dependencies
echo "Installing backend dependencies..."
cd ./MovieObserver/backend
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f "./.env" ]; then
    echo "Creating .env file from template..."
    cp ./.env.example ./.env
fi

# Return to root directory
cd ../..

# Install frontend dependencies
echo "Installing frontend dependencies..."
cd ./MovieObserver/frontend
npm install

# Create .env.local file if it doesn't exist
if [ ! -f "./.env.local" ]; then
    echo "Creating .env.local file..."
    echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > ./.env.local
fi

# Return to root directory
cd ../..

echo "Setup complete!"
echo ""
echo "To start the backend (in a separate terminal):"
echo "  1. Activate the virtual environment: source movieobserver-env/bin/activate"
echo "  2. Run: cd ./MovieObserver/backend"
echo "  3. Run: uvicorn api.main:app --reload"
echo ""
echo "To start the frontend (in a separate terminal):"
echo "  1. Run: cd ./MovieObserver/frontend"
echo "  2. Run: npm run dev"
echo ""
echo "Then open http://localhost:3000 in your browser."
