#!/usr/bin/env python3
"""
Manual Hub installation helper for Prism on Linux
"""

import os
import sys
import json
import urllib.request
import zipfile
import tempfile
import shutil

# Set up paths
script_dir = os.path.dirname(os.path.abspath(__file__))
prism_root = os.path.join(script_dir, "Prism")
plugins_dir = os.path.join(prism_root, "Plugins", "Custom")

sys.path.insert(0, os.path.join(prism_root, "Scripts"))

print("Prism Hub Manual Installer")
print("=" * 50)

# Create plugins directory if it doesn't exist
os.makedirs(plugins_dir, exist_ok=True)

def download_plugin(plugin_name, url=None):
    """Download and install a plugin"""
    print(f"\nDownloading {plugin_name}...")
    
    if not url:
        # These are the typical Prism plugin URLs (you may need to update these)
        base_url = "https://prism-pipeline.com/downloads/plugins/"
        url = f"{base_url}{plugin_name}.zip"
    
    try:
        # Download to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as tmp_file:
            response = urllib.request.urlopen(url)
            tmp_file.write(response.read())
            temp_path = tmp_file.name
        
        print(f"Downloaded to {temp_path}")
        
        # Extract to plugins directory
        target_dir = os.path.join(plugins_dir, plugin_name)
        if os.path.exists(target_dir):
            print(f"Removing existing {plugin_name} directory...")
            shutil.rmtree(target_dir)
        
        print(f"Extracting to {target_dir}...")
        with zipfile.ZipFile(temp_path, 'r') as zip_ref:
            zip_ref.extractall(plugins_dir)
        
        # Clean up temp file
        os.unlink(temp_path)
        
        print(f"✓ {plugin_name} installed successfully!")
        return True
        
    except Exception as e:
        print(f"✗ Failed to install {plugin_name}: {e}")
        return False

# Try to download from GitHub instead
print("\nNote: The official download URLs might not work.")
print("Trying alternative installation from GitHub...")

github_urls = {
    "Hub": "https://github.com/PrismPipeline/Hub/archive/refs/heads/main.zip",
    "PrismInternals": None  # Add URL if available
}

# Manual instructions
print("\n" + "=" * 50)
print("MANUAL INSTALLATION INSTRUCTIONS:")
print("=" * 50)
print("""
Since automatic download might fail, you can manually install the Hub:

1. Contact Prism support or check their website for Hub download links
2. Download the Hub.zip and PrismInternals.zip files
3. Extract them to: {}
4. Restart Prism

The Hub plugin provides:
- Login/account management
- Plugin marketplace
- Automatic updates
- Cloud project sync

Without Hub, you can still use Prism locally but won't have access to:
- Online services
- Plugin marketplace
- Automatic updates
""".format(plugins_dir))

# Check current plugin status
print("\n" + "=" * 50)
print("Current Plugin Status:")
print("=" * 50)

for plugin in ["Hub", "PrismInternals"]:
    plugin_path = os.path.join(plugins_dir, plugin)
    if os.path.exists(plugin_path):
        print(f"✓ {plugin}: Installed at {plugin_path}")
    else:
        print(f"✗ {plugin}: Not installed")

print("\nTo start Prism after installing Hub:")
print("./Prism_safe.sh")