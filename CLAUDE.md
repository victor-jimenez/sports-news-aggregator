# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
A sports news aggregator that extracts news from `marca.com` and `as.com`, clusters overlapping stories, and provides LLM-generated combined summaries.

## Tech Stack
- **Frontend**: Next.js (App Router), Tailwind CSS
- **Backend/Scraping**: Python (BeautifulSoup/Playwright) or Node.js
- **AI/Summarization**: Claude API (Anthropic)
- **Logic**: Custom clustering and ranking algorithm based on front-page position

## Architecture
- `app/`: Next.js frontend and API routes for serving processed news.
- `scraper/`: Independent scripts to fetch and extract raw data from Marca and AS.
- `processor/`: Logic for:
    - **Clustering**: Matching similar articles across sources.
    - **Ranking**: Calculating relevance scores based on position and cross-site presence.
    - **Summarization**: Orchestrating calls to the LLM to merge article content.

## Common Commands
*(To be updated as the project is initialized)*
- Build: `npm run build`
- Dev: `npm run dev`
- Scraper: `python scraper/main.py` (anticipated)
