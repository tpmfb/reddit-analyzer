PROJECT = reddit-cli
IMAGE   = $(PROJECT):latest

.PHONY: build run shell clean scan sbom

build:
	@echo "🐳  Building runtime image..."
	docker build -t $(IMAGE) -f Dockerfile .

run:
	@echo "🚀  Running reddit-cli interactively..."
	docker run --rm -it --env-file .env $(IMAGE)

shell:
	@echo "🔧  Entering container shell..."
	docker run --rm -it --env-file .env --entrypoint /bin/bash $(IMAGE)

scan:
	@echo "🧪  Running security scans (SBOM + CVEs + secrets)..."
	docker build -t $(PROJECT)-scanner -f Dockerfile.security .
	docker run --rm -v $(PWD):/scan $(PROJECT)-scanner
	@echo "✅  scan complete. artifacts: sbom.json, gitleaks.json"

sbom:
	@echo "📦  Generating SBOM only..."
	docker run --rm -v $(PWD):/scan alpine/syft . -o json > sbom.json

clean:
	@echo "🧹  Cleaning up..."
	rm -f sbom.json gitleaks.json || true
	docker rmi $(IMAGE) $(PROJECT)-scanner || true
