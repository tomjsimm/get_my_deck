# Steam Deck Refurbished Stock Checker

A simple scraper which checks the Steam Deck Refurb page for stock. This script sends signal notifications when the Steam Deck is in stock.

## Requirements

- Python (Latest version)
- Selenium WebDriver for Firefox via PIP
- [Signal CLI Rest API](https://github.com/bbernhard/signal-cli-rest-api) for sending notifications

## Getting Started

### Docker

1. Build & run the Docker image:
   ```sh
   make build
   ```
2. Destroy and clean up and local instances:
   ```sh
   make down
   ```

## Environment Variables (Docker)

```
SIGNAL_API_URL=http://localhost:9922
SIGNAL_NUMBER=+1234567890
SEND_TO_NUMBER=+1234567890
TEST_MESSAGE=false
REFRESH_TIME=1800
```

## Credits

- This is a fork of [timoknapp/get_my_deck](https://github.com/timoknapp/get_my_deck).
- Which was a fork of [maroofc/get_my_deck](https://github.com/maroofc/get_my_deck).
