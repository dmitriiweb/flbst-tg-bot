:PHONY format
format:
	ruff check flibusta_bot --select I --fix
	ruff format flibusta_bot

:PHONY lint
lint:
	ruff check flibusta_bot
	mypy flibusta_bot