import subprocess
import os
import time

edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
dest_dir = r"c:\Users\GANPATI\OneDrive\Documents\SKILL_SWAP_FSD\ppt_assets"
os.makedirs(dest_dir, exist_ok=True)

pages = [
    ("shot_01_landing_hero.png", "http://localhost:5173/", "1280,800"),
    ("shot_02_dashboard.png", "http://localhost:5173/dashboard", "1280,850"),
    ("shot_03_my_skills.png", "http://localhost:5173/my-skills", "1280,850"),
    ("shot_04_explore.png", "http://localhost:5173/explore", "1280,850"),
    ("shot_05_smart_match.png", "http://localhost:5173/smart-match", "1280,850"),
    ("shot_06_my_swaps.png", "http://localhost:5173/my-swaps", "1280,850"),
    ("shot_07_manage_profile.png", "http://localhost:5173/manage-profile", "1280,850"),
    ("shot_08_notifications.png", "http://localhost:5173/notifications", "1280,850"),
]

for filename, url, size in pages:
    out_path = os.path.join(dest_dir, filename)
    cmd = [
        edge_path,
        "--headless=new",
        f"--screenshot={out_path}",
        f"--window-size={size}",
        "--hide-scrollbars",
        url
    ]
    print(f"Capturing {url} -> {out_path}...")
    subprocess.run(cmd, check=True)
    time.sleep(1.5)

print("All screenshots captured successfully!")
