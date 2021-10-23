sudo chmod +x /home/ubuntu/scripts/validator.sh
sudo chmod +x /home/ubuntu/scripts/tuner.sh

source tuner.sh

sudo systemctl disable --now sol
sudo cp /home/ubuntu/scripts/sol.service /etc/systemd/system/sol.service
sudo systemctl daemon-reload
sudo systemctl enable --now sol

journalctl -u sol -f