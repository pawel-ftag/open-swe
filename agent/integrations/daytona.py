import os

from daytona import CreateSandboxFromSnapshotParams, Daytona, DaytonaConfig
from langchain_daytona import DaytonaSandbox


def create_daytona_sandbox(sandbox_id: str | None = None):
    api_key = os.getenv("DAYTONA_API_KEY")
    if not api_key:
        raise ValueError("DAYTONA_API_KEY environment variable is required")

    snapshot_name = os.getenv("DEFAULT_SANDBOX_TEMPLATE_NAME", "daytonaio/sandbox:0.6.0")

    daytona = Daytona(config=DaytonaConfig(api_key=api_key))

    if sandbox_id:
        sandbox = daytona.get(sandbox_id)
    else:
        params = CreateSandboxFromSnapshotParams(
            snapshot=snapshot_name,
            auto_stop_interval=60,
        )
        sandbox = daytona.create(params=params)

    return DaytonaSandbox(sandbox=sandbox)


def configure_daytona_git_credentials(sandbox: DaytonaSandbox, github_token: str) -> None:
    """Inject GitHub token into the Daytona sandbox for git operations."""
    sandbox.run_command(
        f'git config --global credential.helper store && '
        f'echo "https://x-access-token:{github_token}@github.com" > /home/daytona/.git-credentials && '
        f'git config --global user.email "bot@formattingtool.ch" && '
        f'git config --global user.name "open-swe-bot"'
    )
