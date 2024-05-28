#!/bin/bash

echo "Starting Container..."
cd /app/mercado_livre && /usr/local/bin/scrapy crawl ocultismo
# Keep the container running
tail -f /dev/null