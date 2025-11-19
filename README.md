🌍 News Location Visualizer
https://img.shields.io/badge/License-MIT-yellow.svg
https://img.shields.io/badge/Python-3.9+-blue.svg
https://img.shields.io/badge/Three.js-3D%2520Visualization-black.svg

An interactive 3D globe that visualizes real-time global news coverage by extracting geographical locations from news articles and plotting them on a spinning globe. Combines web scraping, natural language processing, and 3D visualization technologies.

https://via.placeholder.com/800x400/2c3e50/ffffff?text=3D+News+Globe+Visualization

✨ Features
🔄 Real-time Data Processing
Live News Scraping: Fetches current headlines from major news sources (BBC, NYT, Al Jazeera)

Automated RSS Parsing: Processes multiple RSS feeds simultaneously

Smart Caching: Avoids duplicate articles and optimizes performance

🧠 Intelligent Location Detection
NLP-Powered Geolocation: Uses spaCy to identify Geographical Political Entities (GPEs) in article text

Entity Resolution: Determines the most relevant location per article

Geocoding Integration: Converts location names to precise coordinates using geopy

🎮 Interactive 3D Visualization
Dynamic Globe: Real-time spinning 3D globe built with Three.js and globe.gl

Interactive Points: Click and drag to rotate, hover over points for article details

Responsive Design: Works seamlessly across different screen sizes

🛡️ Local-First Architecture
Self-Contained: Entirely runs on your local machine

CORS Bypass: Uses local Python HTTP server to avoid cross-origin restrictions

Privacy Focused: No data leaves your local environment

🚀 Quick Start
Prerequisites
Ensure you have the following installed:

Python 3.9+ (includes python3 -m http.server)

curl (standard on Linux/macOS, install via WSL on Windows)

