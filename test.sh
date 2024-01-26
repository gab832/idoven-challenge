pushd .
echo "Starting server..."
cd src && DATABASE=sqlite:///./test.db uvicorn main:app &
sleep 3
echo "Server running..."
echo "Running E2E..."
poetry run python e2e_test.py
echo "E2E done..."
kill -9 `pgrep -f uvicorn`
echo "Server killed "
rm src/test.db
popd
