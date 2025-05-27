#!/bin/bash

SERVICE_NAME="gangboss"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
REPO_URL="https://github.com/AmirKenzo/GangBoss-DiscordBot.git"
BOT_DIR="/root/GangBoss-DiscordBot"
UV_PATH="/root/.local/bin/uv"

function install_uv() {
    echo "Cloning bot repository into $BOT_DIR ..."
    if [ ! -d "$BOT_DIR" ]; then
        git clone "$REPO_URL" "$BOT_DIR"
    else
        echo "Bot directory already exists, skipping clone."
    fi

    echo "Installing uv runtime..."
    curl -LsSf https://astral.sh/uv/install.sh | sh

    if [ -f "$HOME/.local/bin/env" ]; then
        echo "Sourcing uv environment..."
        source "$HOME/.local/bin/env"
    else
        echo "env file not found. uv may not be properly installed."
    fi
    echo "Creating systemd service file at $SERVICE_FILE ..."
    sudo tee "$SERVICE_FILE" > /dev/null <<EOF
[Unit]
Description=GangBoss Discord Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$BOT_DIR
ExecStartPre=/bin/sleep 5
ExecStart=$UV_PATH run main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

    echo "Reloading systemd daemon..."
    sudo systemctl daemon-reload

    echo "Enabling $SERVICE_NAME service to start on boot..."
    sudo systemctl enable "$SERVICE_NAME"

    echo "Installing gangboss command in /usr/local/bin ..."
    sudo cp "$BOT_DIR/install.sh" /usr/local/bin/gangboss
    sudo chmod +x /usr/local/bin/gangboss
    echo "✅ You can now use the 'gangboss' command globally!"


}

function clone_or_update() {
    if [ -d "$BOT_DIR" ]; then
        echo "Directory exists. Updating repo..."
        cd "$BOT_DIR" || exit
        git pull origin main
        cd ..
    else
        echo "Cloning repo..."
        git clone "$REPO_URL"
    fi
}

function edit_env() {
    cd "$BOT_DIR" || exit

    if [ ! -f ".env" ]; then
        if [ -f ".env.example" ]; then
            echo ".env not found. Copying from .env.example..."
            cp .env.example .env
        else
            echo "No .env or .env.example found."
            cd ..
            return
        fi
    fi

    echo "Opening .env with nano..."
    nano .env
    cd ..
}



run() {
    if [ ! -f "$SERVICE_FILE" ]; then
        create_service
    fi

    echo "Starting $SERVICE_NAME service..."
    sudo systemctl start "$SERVICE_NAME"
}

stop() {
    echo "Stopping $SERVICE_NAME service..."
    sudo systemctl stop "$SERVICE_NAME"
}

restart() {
    echo "Restarting $SERVICE_NAME service..."
    sudo systemctl restart "$SERVICE_NAME"
}

status() {
    sudo systemctl status "$SERVICE_NAME"
}

logs() {
    sudo journalctl -u "$SERVICE_NAME" -f
}

remove() {
    echo "Stopping and disabling $SERVICE_NAME service..."
    sudo systemctl stop "$SERVICE_NAME"
    sudo systemctl disable "$SERVICE_NAME"
    echo "Removing service file $SERVICE_FILE..."
    sudo rm -f "$SERVICE_FILE"
    echo "Reloading systemd daemon..."
    sudo systemctl daemon-reload
}


usage() {
    local script_name="${0##*/}"
    echo -e "\e[34m==============================\e[0m"
    echo -e "\e[35m         GangBoss Help        \e[0m"
    echo -e "\e[34m==============================\e[0m"
    echo -e "\e[36mUsage:\e[0m"
    echo "  ${script_name} [command]"
    echo

    echo -e "\e[36mCommands:\e[0m"
    echo -e "\e[33m  install     \e[0m– Install uv runtime and prepare environment"
    echo -e "\e[33m  update      \e[0m– Pull latest changes from GitHub"
    echo -e "\e[33m  run         \e[0m– Start the bot"
    echo -e "\e[33m  stop        \e[0m– Stop the bot"
    echo -e "\e[33m  remove      \e[0m– Remove bot files and stop"
    echo -e "\e[33m  edit        \e[0m– Edit .env file via nano (create if missing)"
    echo -e "\e[33m  help        \e[0m– Show this help message"
    echo

    echo -e "\e[36mDirectories:\e[0m"
    echo -e "\e[35m  Bot directory: /path/to/bot\e[0m"
    echo -e "\e[35m  Data directory: /path/to/data\e[0m"
    echo -e "\e[34m==============================\e[0m"
    echo
}

case "$1" in
    install)
        install_uv
        ;;
    update)
        clone_or_update
        ;;
    run)
        run_bot
        ;;
    edit)
        edit_env
        ;;
    stop)
        stop_bot
        ;;
    remove)
        remove_bot
        ;;
    *)
        usage
        ;;
esac
