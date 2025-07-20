# Flibusta Telegram Bot

A multilingual Telegram bot for searching and downloading books from multiple libraries including Flibusta and Project Gutenberg. The bot provides an intuitive interface for finding books by title or author, with support for multiple languages and various download formats.

## Features

- **Multi-library Support**: Search across Flibusta and Project Gutenberg
- **Multiple Search Methods**: 
  - Search books by title
  - Search books by author
- **Multilingual Interface**: Support for 30+ languages including English, Russian, Spanish, French, German, and more
- **Download Management**: Browse and download books in various formats
- **Pagination**: Navigate through search results efficiently
- **Webhook Support**: Can run with webhooks for production deployments
- **Logging**: Comprehensive logging with rotation and retention policies

## Supported Languages

The bot supports the following languages:
- Arabic (ar)
- Azerbaijani (az) 
- Bulgarian (bg)
- German (de)
- English (en)
- Spanish (es)
- Persian (fa)
- Finnish (fi)
- French (fr)
- Hebrew (he)
- Hindi (hi)
- Indonesian (id)
- Italian (it)
- Japanese (ja)
- Kazakh (kk)
- Korean (ko)
- Mongolian (mn)
- Dutch (nl)
- Polish (pl)
- Portuguese (pt)
- Romanian (ro)
- Russian (ru)
- Tajik (tg)
- Thai (th)
- Turkish (tr)
- Ukrainian (uk)
- Uzbek (uz)
- Chinese Simplified (zh-hans)
- Chinese Traditional (zh-hant)

## Technology Stack

- **Python 3.12+**
- **aiogram 3.x** - Telegram Bot API framework
- **fluentogram** - Internationalization (i18n)
- **httpx** - HTTP client for API requests
- **lxml** - XML/HTML parsing
- **loguru** - Logging
- **Docker** - Containerization
- **uv** - Fast Python package manager

## Prerequisites

- Docker and Docker Compose
- Telegram Bot Token (obtain from [@BotFather](https://t.me/BotFather))

## Quick Start with Docker

### 1. Clone the Repository

```bash
git clone git@github.com:dmitriiweb/flbst-tg-bot.git
cd flbst-tg-bot
```

### 2. Configure Environment

Create a `.env` file in the project root:

```bash
# Required: Your Telegram Bot Token
TG_BOT_TOKEN=your_bot_token_here

# Optional: Bot configuration
TG_BOT_NAME=your_bot_name
BASE_URL=https://flibusta.is

# Optional: Webhook configuration (for production)
TG_BOT_WEBHOOK_BASE_URL=https://your-domain.com
TG_BOT_WEBHOOK_PATH=/webhook
TG_BOT_WEBHOOK_SECRET=your_webhook_secret

# Optional: Web server configuration
WEB_SERVER_HOST=0.0.0.0
WEB_SERVER_PORT=8000

# Optional: Database configuration (if using PostgreSQL)
POSTGRES_DB=flibusta_bot
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

### 3. Build and Run

```bash
# Build and start the container
docker-compose up --build

# Or run in detached mode
docker-compose up --build -d
```

### 4. Access Your Bot

The bot will be available on Telegram. Start a conversation with your bot and use the `/start` command to begin.

## Docker Configuration

The project includes a complete Docker setup with the following configuration:

### Services

- **flibusta-tg-bot**: Main application container
  - Port: `9998:8000` (host:container)
  - Restart policy: Always
  - Volumes mounted:
    - `./flibusta_bot:/app/flibusta_bot` - Application code
    - `./logs:/app/logs` - Log files
    - `./locales:/app/locales` - Translation files

### Network

- Custom bridge network: `flibusta-tg-bot-network`

### System Configuration

- Increased connection limit: `net.core.somaxconn: 65536`

## Development

### Local Development Setup

1. Install dependencies:
```bash
uv sync --all-extras
```

2. Run the bot in Docker container:
```bash
docker-compose up --build
```

**Note**: The bot is designed to run in a Docker container. For local development, use the Docker setup to ensure consistency with the production environment.

### Code Quality

The project includes code quality tools configured in the Makefile:

```bash
# Format code
make format

# Lint and type check
make lint
```

### Project Structure

```
flibusta-bot/
├── flibusta_bot/           # Main application
│   ├── parsers/           # Library parsers (Flibusta, Gutenberg)
│   ├── tg_bot/            # Telegram bot implementation
│   │   ├── handlers/      # Message handlers
│   │   ├── keyboards/     # Inline keyboards
│   │   ├── middlewares/   # Bot middlewares
│   │   └── states.py      # FSM states
│   └── config.py          # Configuration
├── locales/               # Translation files
├── logs/                  # Application logs
├── docker-compose.yaml    # Docker Compose configuration
├── Dockerfile            # Docker image definition
└── pyproject.toml        # Project dependencies
```

## Configuration Options

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `TG_BOT_TOKEN` | Telegram Bot API token | - | Yes |
| `TG_BOT_NAME` | Bot display name | - | No |
| `BASE_URL` | Flibusta base URL | `https://flibusta.is` | No |
| `TG_BOT_WEBHOOK_BASE_URL` | Webhook base URL | - | No |
| `TG_BOT_WEBHOOK_PATH` | Webhook path | `/webhook` | No |
| `TG_BOT_WEBHOOK_SECRET` | Webhook secret token | - | No |
| `WEB_SERVER_HOST` | Web server host | `0.0.0.0` | No |
| `WEB_SERVER_PORT` | Web server port | `8000` | No |

## Logging

The application uses structured logging with Loguru:

- **Info logs**: `logs/info.log`
- **Error logs**: `logs/error.log`
- **Rotation**: 10 MB per file
- **Retention**: 10 days

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting: `make lint`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Known Bots

- [Search in the Library Bot](https://t.me/search_in_the_library_bot) - Live example of this bot

## Support

For issues and questions, please open an issue on GitHub or contact the maintainers.
