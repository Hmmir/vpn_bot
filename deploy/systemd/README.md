# systemd setup

## Install

```bash
sudo cp /home/web/vpn_bot/deploy/systemd/getnius-bot.service /etc/systemd/system/
sudo cp /home/web/vpn_bot/deploy/systemd/getnius-support.service /etc/systemd/system/
sudo cp /home/web/vpn_bot/deploy/systemd/getnius-webhook.service /etc/systemd/system/
sudo cp /home/web/vpn_bot/deploy/systemd/getnius-healthcheck.service /etc/systemd/system/
sudo cp /home/web/vpn_bot/deploy/systemd/getnius-healthcheck.timer /etc/systemd/system/
sudo cp /home/web/vpn_bot/deploy/systemd/getnius-updatecheck.service /etc/systemd/system/
sudo cp /home/web/vpn_bot/deploy/systemd/getnius-updatecheck.timer /etc/systemd/system/

sudo systemctl daemon-reload
sudo systemctl enable --now getnius-bot.service
sudo systemctl enable --now getnius-support.service
sudo systemctl enable --now getnius-webhook.service
sudo systemctl enable --now getnius-healthcheck.timer
sudo systemctl enable --now getnius-updatecheck.timer
```

## Logs

```bash
sudo journalctl -u getnius-bot.service -f
sudo journalctl -u getnius-support.service -f
sudo journalctl -u getnius-webhook.service -f
sudo journalctl -u getnius-healthcheck.service -f
sudo journalctl -u getnius-updatecheck.service -f
```

## Restart

```bash
sudo systemctl restart getnius-bot.service
sudo systemctl restart getnius-support.service
sudo systemctl restart getnius-webhook.service
sudo systemctl restart getnius-healthcheck.service
sudo systemctl restart getnius-updatecheck.service
```
