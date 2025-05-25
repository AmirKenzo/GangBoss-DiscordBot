CMD="source /home/loserbo1/virtualenv/kenzobot/3.12/bin/activate && cd /home/loserbo1/kenzobot"

if screen -ls | grep bot1 | grep Detached &>/dev/null; then
    echo "Running"
else
    bash -c "$CMD && screen -d -m -S bot1 uv run main.py"
fi
