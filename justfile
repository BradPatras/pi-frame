default:
    just --list

[working-directory('config-interface-frontend')]
build-frontend:
    npm run build

[working-directory('config-interface-frontend')]
start-frontend: build-frontend
    python -m http.server 50002 --directory dist

[working-directory('config-interface-backend')]
start-backend:
    gunicorn -w 2 -b 0.0.0.0:50001 server:app

[parallel]
start-both: start-frontend start-backend

build-frame: build-frontend
    rm -rf dist/
    mkdir dist/
    mkdir dist/frame

    mkdir dist/frame/config-interface-backend
    cp -R config-interface-backend/ dist/frame/config-interface-backend/
    rm -rf dist/frame/config-interface-backend/__pycache__

    mkdir dist/frame/config-interface-frontend
    cp -R config-interface-frontend/dist/ dist/frame/config-interface-frontend/

    mkdir dist/frame/frame-interface
    cp -R frame-interface/ dist/frame/frame-interface/
    rm -rf dist/frame/frame-interface/__pycache__

    cp install.sh dist/frame/
    cp photo-display.service dist/frame/
    cp start-hotspot.sh dist/frame/
    cp stop-hotspot.sh dist/frame/
    cp start-frame.sh dist/frame/
    cp requirements.txt dist/frame/
