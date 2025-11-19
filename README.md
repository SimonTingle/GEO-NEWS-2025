🌍 News Location Visualizer
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Three.js](https://img.shields.io/badge/Three.js-3D%20Visualization-black.svg)](https://threejs.org/)
[![Status](https://img.shields.io/badge/Status-Beta-orange.svg)](https://github.com)

License: MIT Python Three.js Status

An interactive 3D globe that visualizes real-time global news coverage by extracting geographical locations from news articles and plotting them on a spinning globe. Combines web scraping, natural language processing, and 3D visualization technologies.

3D News Globe Visualization
✨ Features

🔄 Real-time Data Processing

Live News Scraping: Fetches current headlines from major news sources (BBC, NYT, Al Jazeera, Reuters)
Automated RSS Parsing: Processes multiple RSS feeds simultaneously with concurrent processing
Smart Caching: Avoids duplicate articles and optimizes performance with intelligent caching mechanisms
Rate Limiting: Respects API limits and prevents server overload
🧠 Intelligent Location Detection

NLP-Powered Geolocation: Uses spaCy to identify Geographical Political Entities (GPEs) in article text
Entity Resolution: Determines the most relevant location per article using context analysis
Geocoding Integration: Converts location names to precise coordinates using geopy with fallback providers
Disambiguation: Resolves ambiguous location names using population data and context clues
🎮 Interactive 3D Visualization

Dynamic Globe: Real-time spinning 3D globe built with Three.js and globe.gl
Interactive Points: Click and drag to rotate, hover over points for article details, zoom with scroll
Responsive Design: Works seamlessly across different screen sizes and devices
Customizable Themes: Multiple color schemes and visualization modes
Animation Controls: Play/pause globe rotation, adjust animation speed
🛡️ Local-First Architecture

Self-Contained: Entirely runs on your local machine with no external dependencies
CORS Bypass: Uses local Python HTTP server to avoid cross-origin restrictions
Privacy Focused: No data leaves your local environment
Offline Mode: Cache functionality allows offline browsing of recent news
🚀 Quick Start

Prerequisites

Ensure you have the following installed:

Python 3.9+ (includes python3 -m http.server)
curl (standard on Linux/macOS, install via WSL on Windows)
pip (Python package installer)

