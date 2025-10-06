# Dockerfile complet
FROM python:3.12-bookworm

# éviter les prompts interactifs
ENV DEBIAN_FRONTEND=noninteractive

# installer dépendances système (tesseract + libs)
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      tesseract-ocr \
      libtesseract-dev \
      libleptonica-dev \
      pkg-config \
 && rm -rf /var/lib/apt/lists/*

# définir un répertoire de travail
WORKDIR /workspace

# installer dépendances Python de base
RUN pip install --no-cache-dir pillow pytesseract opencv-python-headless
# RUN pip install duckdb pandas   plutôt dans requirements.txt et devcontainer.json
