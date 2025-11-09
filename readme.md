# r00m101 Reddit CLI

A command-line interface (CLI) tool for interacting with the r00m101 API, enabling analysis of Reddit usernames, retrieval of user comment history, listing of subreddit subscribers, and searching Reddit submissions.

## Features

- **Analyze Usernames**: Use AI models to analyze Reddit user profiles, including behavioral patterns, interests, and potential risks.
- **Fetch User History**: Download a user's comment history as CSV for offline analysis.
- **Subreddit Subscribers**: Retrieve subscriber counts and details for subreddits.
- **Search Submissions**: Perform advanced searches on Reddit submissions by keywords and time ranges.
- **Quota Management**: Check your API usage quota.
- **Multiple AI Models**: Supports various AI models including Grok, Gemini, DeepSeek, and Llama variants.
- **Flexible Configuration**: Supports environment variables or `.env` files for API key management.

## Important: API Key Required

This tool requires a valid API key (Bearer token) from r00m101.com. Purchase an API key at [https://r00m101.com](https://r00m101.com) to access the API endpoints.

**Security Note**: Never commit your API key to version control. Use environment variables or a local `.env` file, and ensure `.env` is listed in `.gitignore`.

## Installation

### Prerequisites

- Python 3.8 or higher
- pip for package management

### Install Dependencies

Clone the repository and install required packages:

```bash
git clone <repository-url>
cd r00m101
pip install -r requirements.txt
```

Required packages:
- `requests==2.32.5` - For HTTP API calls
- `python-dotenv==1.1.1` - For loading environment variables from `.env` file

## Configuration

### API Key Setup

1. **Using `.env` file** (recommended):
   Create a `.env` file in the project root:
   ```
   Bearer=YOUR_API_KEY_HERE
   ```
   Replace `YOUR_API_KEY_HERE` with your purchased API key.

2. **Using environment variable**:
   ```bash
   export Bearer="YOUR_API_KEY_HERE"
   ```

If no API key is provided, the tool will prompt for it on first use.

## Usage

Run the CLI:

```bash
python reddit_r00m.py
```

The tool presents an interactive menu with the following options:

1. **Analyze Username**: Analyze a Reddit user's profile
   - Prompts for username, AI model selection, and analysis options
   - Options include fetching latest messages, forcing re-processing, verifying sources
   - Supports use case specification (e.g., law enforcement)

2. **Get Username History**: Download user comment history as CSV
   - Prompts for username and whether to fetch latest messages
   - Outputs CSV data directly to console

3. **Get Subreddit Subscribers**: Retrieve subreddit subscriber information
   - Prompts for subreddit name (without r/)
   - Returns JSON with subscriber details

4. **Search Submissions**: Search Reddit submissions
   - Prompts for search terms (comma-separated)
   - Optional timestamp filters (Unix timestamps)
   - Returns JSON with matching submissions

5. **Check Quota**: View current API usage quota
   - Displays remaining API calls and limits

### Available AI Models

The analysis feature supports the following models:
- x-ai/grok-3-mini
- x-ai/grok-4
- x-ai/grok-4-fast
- google/gemini-2.0-flash-001
- google/gemini-2.0-flash-lite-001
- google/gemini-2.5-flash
- google/gemini-2.5-flash-lite
- google/gemini-2.5-pro
- deepseek/deepseek-chat-v3-0324
- deepseek/deepseek-r1-0528
- deepseek/deepseek-r1-0528:free
- nvidia/llama-3.1-nemotron-ultra-253b-v1:free

### Example Usage

```bash
# Run the CLI
python reddit_r00m.py

# Menu appears:
# Choose an option:
# 1. Analyze username
# 2. Get username history
# 3. Get subreddit subscribers
# 4. Search submissions
# 5. Check quota
# Q. Quit

# Select option 1, then follow prompts:
# Enter Reddit username: exampleuser
# Available models:
# 1. x-ai/grok-3-mini
# ...
# Pick a model by number or provide a model string: 1
# Fetch latest messages? (true/false): true
# Force re-processing? (true/false): false
# Verify sources? (true/false): true
# Use case (leave blank or type 'law_enforcement'):
```

## Docker Usage

### Build the image

```bash
docker-compose build
```

or

```bash
docker build -t reddit-analyzer .
```

This will:
- Build the Docker image with Python and dependencies
- Load environment variables from `.env`
- Run the CLI in interactive mode

### Using the Makefile

The project includes a `Makefile` with convenient shortcuts for common Docker operations:

- `make build`: Builds the Docker image.
- `make run`: Runs the CLI interactively with environment variables loaded.
- `make shell`: Opens a bash shell inside the container.
- `make scan`: Runs security scans (builds scanner image, checks for vulnerabilities and secrets).
- `make sbom`: Generates a Software Bill of Materials (SBOM) file.
- `make clean`: Removes built images and generated files.

Example:

```bash
make build
make run
```

This simplifies Docker workflows without remembering full commands.

## API Endpoints

The tool interacts with the following r00m101 API endpoints:
- `GET /quota` - Check API quota
- `GET /analyze/{username}` - Analyze user profile
- `GET /user/{username}` - Get user comment history (CSV)
- `GET /subreddit/{subreddit}` - Get subreddit subscribers
- `GET /search` - Search submissions

All endpoints require Bearer token authentication.

## Security Considerations

- API keys are sensitive; never expose them in code or version control
- The tool uses HTTPS for all API communications
- No hardcoded credentials or secrets in the codebase
- Environment variables are used for configuration to avoid accidental exposure

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Support

For API key purchases and support, visit [https://r00m101.com](https://r00m101.com).