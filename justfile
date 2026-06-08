default:
    just --list

[working-directory('frame-config-frontend')]
dev-frontend:
    npm run dev

[working-directory('frame-config-frontend')]
build-frontend:
    npm run build

[working-directory('frame-config-frontend')]
start-frontend: build-frontend
    npm run dev -- --port 50002

[working-directory('frame-config-backend')]
start-backend:
    gunicorn -w 2 -b 0.0.0.0:50001 server:app

[parallel]
start-both: start-frontend start-backend

build-frame: build-frontend
    rm -rf dist/
    mkdir dist/
    mkdir dist/frame

    mkdir dist/frame/frame-config-backend
    cp -R frame-config-backend/ dist/frame/frame-config-backend/
    rm -rf dist/frame/frame-config-backend/__pycache__

    mkdir dist/frame/frame-config-frontend
    cp -R frame-config-frontend/dist/ dist/frame/frame-config-frontend/

    mkdir dist/frame/frame-core
    cp -R frame-core/ dist/frame/frame-core/
    rm -rf dist/frame/frame-core/__pycache__

    cp install.sh dist/frame/
    cp photo-display.service dist/frame/
    cp start-hotspot.sh dist/frame/
    cp stop-hotspot.sh dist/frame/
    cp start-frame.sh dist/frame/
    cp requirements.txt dist/frame/
