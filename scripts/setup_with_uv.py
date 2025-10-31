#!/usr/bin/env python
"""
UV Setup Script for PDF RAG MCP Server
Automates environment setup with UV package manager
"""

import subprocess
import sys
import platform
from pathlib import Path
from typing import Tuple


def run_command(cmd: list[str], description: str = "") -> Tuple[bool, str]:
    """Run a command and return success status and output"""
    print(f"\n{'='*70}")
    if description:
        print(f"📌 {description}")
    print(f"{'='*70}")
    print(f"Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✅ Success!")
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        print(f"Output: {e.stderr}")
        return False, e.stderr
    except FileNotFoundError:
        print(f"❌ Command not found: {cmd[0]}")
        return False, f"Command not found: {cmd[0]}"


def check_uv_installed() -> bool:
    """Check if UV is installed"""
    success, _ = run_command(["uv", "--version"], "Checking UV installation")
    return success


def install_uv() -> bool:
    """Install UV package manager"""
    os_name = platform.system()
    print(f"\n{'='*70}")
    print(f"Installing UV for {os_name}")
    print(f"{'='*70}")
    
    if os_name == "Windows":
        success, _ = run_command(
            ["powershell", "-Command", "irm https://astral.sh/uv/install.ps1 | iex"],
            "Installing UV on Windows"
        )
    elif os_name == "Darwin":
        success, _ = run_command(
            ["curl", "-LsSf", "https://astral.sh/uv/install.sh", "|", "sh"],
            "Installing UV on macOS"
        )
    else:  # Linux
        success, _ = run_command(
            ["bash", "-c", "curl -LsSf https://astral.sh/uv/install.sh | sh"],
            "Installing UV on Linux"
        )
    
    if success:
        print("\n✅ UV installed successfully!")
        print("⚠️  You may need to restart your terminal or add UV to PATH")
        return True
    else:
        print("\n❌ Failed to install UV")
        print("Please visit: https://docs.astral.sh/uv/")
        return False


def setup_project() -> bool:
    """Setup project with UV"""
    import os
    base_dir = Path(__file__).parent.parent
    os.chdir(base_dir)
    
    print(f"\n{'='*70}")
    print("🚀 PDF RAG MCP Server - UV Setup")
    print(f"{'='*70}")
    print(f"Project directory: {base_dir}")
    
    # Step 1: Check/Install UV
    if not check_uv_installed():
        print("\n❌ UV not found. Install UV? (y/n): ", end="")
        if input().lower() == 'y':
            if not install_uv():
                print("❌ Cannot continue without UV")
                return False
        else:
            print("❌ UV is required to continue")
            return False
    
    # Step 2: Create Virtual Environment
    print(f"\n{'='*70}")
    print("Step 1: Creating Virtual Environment")
    print(f"{'='*70}")
    
    venv_path = base_dir / ".venv"
    if venv_path.exists():
        print(f"✅ Virtual environment already exists: {venv_path}")
    else:
        success, _ = run_command(
            ["uv", "venv"],
            "Creating virtual environment"
        )
        if not success:
            return False
    
    # Step 3: Install Dependencies
    print(f"\n{'='*70}")
    print("Step 2: Installing Dependencies")
    print(f"{'='*70}")
    
    dev_mode = input("Install with development tools? (y/n) [default: y]: ").lower()
    dev_mode = dev_mode != 'n'
    
    install_cmd = [
        "uv", "pip", "install", "-e",
        ".[dev]" if dev_mode else "."
    ]
    
    success, _ = run_command(install_cmd, "Installing project dependencies")
    if not success:
        return False
    
    # Step 4: Generate Lock File
    print(f"\n{'='*70}")
    print("Step 3: Generating Lock File")
    print(f"{'='*70}")
    
    success, _ = run_command(
        ["uv", "lock"],
        "Generating uv.lock file"
    )
    if not success:
        print("⚠️  Warning: Could not generate lock file")
        # Non-fatal error
    
    # Step 5: Verify Installation
    print(f"\n{'='*70}")
    print("Step 4: Verifying Installation")
    print(f"{'='*70}")
    
    success, output = run_command(
        ["uv", "pip", "list"],
        "Listing installed packages"
    )
    
    if success:
        print("✅ Dependencies installed successfully!")
    else:
        print("⚠️  Warning: Could not verify installation")
    
    # Step 6: Create Directories
    print(f"\n{'='*70}")
    print("Step 5: Creating Data Directories")
    print(f"{'='*70}")
    
    dirs = [
        base_dir / "data" / "vector_stores",
        base_dir / "data" / "document_cache",
        base_dir / "data" / "metadata",
        base_dir / "logs"
    ]
    
    for dir_path in dirs:
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"✅ Created: {dir_path}")
    
    # Step 7: Download Embedding Model
    print(f"\n{'='*70}")
    print("Step 6: Preparing Embedding Model")
    print(f"{'='*70}")
    
    print("Note: Embedding model will be downloaded on first use (~80 MB)")
    print("This will happen automatically when you first run the server")
    
    return True


def print_next_steps(base_dir: Path) -> None:
    """Print next steps for user"""
    os_name = platform.system()
    
    print(f"\n{'='*70}")
    print("🎉 Setup Complete!")
    print(f"{'='*70}")
    
    print("\n📋 Next Steps:")
    print("-" * 70)
    
    # Activation
    if os_name == "Windows":
        print("1. Activate virtual environment:")
        print(f"   {base_dir}\\.venv\\Scripts\\activate")
    else:
        print("1. Activate virtual environment:")
        print(f"   source {base_dir}/.venv/bin/activate")
    
    print("\n2. Run the server:")
    print("   uv run python src/rag_server.py")
    
    print("\n3. In another terminal, test with client:")
    print("   uv run python client.py --help")
    
    print("\n4. Configure Claude Desktop:")
    print("   See CLAUDE_DESKTOP_SETUP.md for details")
    
    print("\n📚 Useful UV Commands:")
    print("-" * 70)
    print("  uv pip list              - List installed packages")
    print("  uv lock --upgrade        - Update dependencies")
    print("  uv run pytest            - Run tests")
    print("  uv run black .           - Format code")
    print("  uv run ruff check .      - Lint code")
    print("  uv run mypy src/         - Type check")
    
    print("\n📖 Documentation:")
    print("-" * 70)
    print("  README.md                - Quick start guide")
    print("  UV_INTEGRATION.md        - Detailed UV guide")
    print("  CONFIG.md                - Configuration reference")
    print("  CLAUDE_DESKTOP_SETUP.md  - Claude Desktop setup")
    
    print("\n🔗 Resources:")
    print("-" * 70)
    print("  UV Docs: https://docs.astral.sh/uv/")
    print("  GitHub:  https://github.com/astral-sh/uv")
    
    print("\n" + "="*70)
    print("✅ Ready to start! Happy coding! 🚀")
    print("="*70 + "\n")


def main() -> int:
    """Main setup function"""
    try:
        base_dir = Path(__file__).parent.parent
        
        # Run setup
        if setup_project():
            print_next_steps(base_dir)
            return 0
        else:
            print("\n❌ Setup failed. Please check the errors above.")
            return 1
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup cancelled by user")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
