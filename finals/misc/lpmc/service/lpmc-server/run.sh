#!/bin/bash
cd "$(dirname "$0")"
exec java -Xms4G -Xmx4G -jar paper-1.8.8-445.jar nogui
