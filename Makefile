.PHONY: deploy

DARKSTAR=jdibling@darkstar

deploy:
	ssh $(DARKSTAR) "mkdir -p ~/homelab"
	rsync -av --exclude='.git' --exclude='.env' . $(DARKSTAR):~/homelab/
	ssh $(DARKSTAR) "cd ~/homelab && docker compose build && docker compose up -d"