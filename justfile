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
    rm -rf dist
    mkdir dist

    mkdir dist/config-interface-backend
    cp -R config-interface-backend dist/
    rm -rf dist/config-interface-backend/__pycache__

    mkdir dist/config-interface-frontend
    cp -R config-interface-frontend/dist dist/

    mkdir dist/frame-interface
    cp -R frame-interface/ dist/
    rm -rf dist/frame-interface/__pycache__

    cp install.sh dist/
    cp photo-display.service dist/
    cp start-hotspot.sh dist/
    cp stop-hotspot.sh dist/
    cp start-frame.sh dist/
