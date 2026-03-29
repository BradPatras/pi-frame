set windows-shell := ["powershell.exe", "-c"]

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
