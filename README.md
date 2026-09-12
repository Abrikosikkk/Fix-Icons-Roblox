# fix_iconsroblox

A small Windows utility that restores broken thumbnails, avatars, and icons in Roblox by resolving `tr.rbxcdn.com` to a working IP address and patching the system `hosts` file.

Repository: https://github.com/Abrikosikkk/Fix-Icons-Roblox

---

## The Problem

Roblox serves all game thumbnails, user avatars, badges, and catalog images from its CDN: `tr.rbxcdn.com`

In some regions (notably Russia and other countries with network filtering), this domain may resolve to a blackholed or unreachable IP. As a result:

- Game icons show as grey squares or blank placeholders
- User avatars fail to load in the friends list and on profiles
- Catalog, store, and inventory images are missing
- Some UI elements appear broken even though the game itself runs fine

This is not a bug in Roblox and not a problem with your files. It is a DNS / routing issue between your machine and the Roblox CDN.

---

## How It Works

The script performs three steps. First, it checks for administrator privileges, because modifying the `hosts` file requires elevation. Second, it resolves a working IP for `tr.rbxcdn.com` by querying public DNS servers (`9.9.9.9` and `1.1.1.1`) that are typically not affected by regional filtering. Third, it writes a static entry to the Windows `hosts` file pinning the domain to the resolved IP, then flushes the DNS cache so the change takes effect immediately.

Once the entry is in place, Windows will always connect to a working CDN node for that domain, and your images will start loading again.

---

## Requirements

- Windows 10 or Windows 11
- Python 3.8 or newer (only if running from source)
- Administrator privileges (required to edit `hosts`)
- An internet connection to a DNS resolver that is not blocked (Quad9 and Cloudflare are used by default)

No third-party Python packages are needed. The script uses only the standard library.

---

## Installation

Option 1 — Clone the repository:

    git clone https://github.com/Abrikosikkk/Fix-Icons-Roblox.git
    cd Fix-Icons-Roblox
    python fix_icons_roblox.py

Option 2 — Download the raw script directly:

    https://github.com/Abrikosikkk/Fix-Icons-Roblox/blob/main/fix_icons_roblox.py

Save it anywhere on your machine, for example on your Desktop.

---

## Usage

Right-click `fix_icons_roblox.py` and choose "Run as administrator", or open an elevated Command Prompt or PowerShell and run:

    python fix_icons_roblox.py

The script will print environment info (target domain, hosts path, DNS servers), resolve the current IP for `tr.rbxcdn.com`, patch the `hosts` file, and flush the DNS cache.

After that, fully close Roblox (including the system tray icon) and relaunch it. Images, avatars, and thumbnails should now load.

Example output:

      ┌─────────────────────────────────────────────┐
      │  fix_icons_roblox.py                        │
      │  Roblox CDN Resolver · v1.0                 │
      └─────────────────────────────────────────────┘

      · target  : tr.rbxcdn.com
      · hosts   : C:\Windows\System32\drivers\etc\hosts
      · dns     : 9.9.9.9, 1.1.1.1

      [1/3] Резолвим актуальный IP…
            → запрос через 9.9.9.9
            ✓ ответ: 18.238.x.x

      [2/3] Обновляем системный hosts…
      ✓ hosts пропатчен → 18.238.x.x tr.rbxcdn.com

      [3/3] Сбрасываем кэш…
      ✓ DNS-кэш очищен

      ─────────────────────────────────────────────
      ✓ Готово. Перезапусти Roblox.
      ─────────────────────────────────────────────

---

## What Gets Changed

The script appends one line to `C:\Windows\System32\drivers\etc\hosts`. It looks like this:

    18.238.x.x tr.rbxcdn.com

The script also removes any previous entries it may have added for the same domain, so re-running it is always safe and idempotent. Nothing else on your system is touched.

---

## Troubleshooting

If the script says "Нет прав на запись в hosts", you did not launch it as administrator. Close the window and re-run it via "Run as administrator".

If it says "Не удалось получить IP ни от одного резолвера", both `9.9.9.9` and `1.1.1.1` failed to respond. This can happen if your ISP blocks these DNS servers (try a VPN to reach the script's own download), if you are behind a captive portal, or if your firewall is blocking `nslookup`. As a workaround, manually change your system DNS to `9.9.9.9` or `1.1.1.1` in Network Adapter Settings, then re-run the script.

If images still don't load after running the script, first make sure Roblox was fully restarted, not just minimized. Check Task Manager for any lingering `RobloxPlayerBeta.exe` processes. Then verify the entry landed in `hosts` by running:

    type C:\Windows\System32\drivers\etc\hosts

Flush DNS manually:

    ipconfig /flushdns

If it still fails, the resolved IP may have gone stale. Just re-run the script and it will grab a fresh IP.

If your antivirus flags the script, note that some AV products treat any `hosts` modification as suspicious. This script is fully open-source, so read the code yourself and then whitelist it.

---

## Uninstalling / Reverting

To undo everything the script did, open `C:\Windows\System32\drivers\etc\hosts` in Notepad as administrator, delete the line containing `tr.rbxcdn.com`, and save the file. Then run `ipconfig /flushdns` in an elevated Command Prompt. That's it. No registry keys, no services, no background processes. The script is a one-shot tool.

---

## FAQ

Does this affect my Roblox account or get me banned? No. It only changes how your computer resolves one image CDN hostname. It does not modify the game, its memory, or communicate with Roblox servers in any unauthorized way.

Will this break other websites? No. The change is scoped to a single domain, `tr.rbxcdn.com`.

Do I need to run it every time I open Roblox? No. The `hosts` entry is persistent. Re-run the script only if images stop loading again, because CDN IPs occasionally rotate.

Why not just use a VPN? A VPN works too, but it routes all your traffic and often adds latency to gameplay. Patching `hosts` is more surgical. You only fix the CDN connection while everything else stays on your normal route.

Does it work on macOS or Linux? The current version targets Windows only. On macOS and Linux the same idea works with `/etc/hosts` instead of `C:\Windows\System32\drivers\etc\hosts`, but you will need to adapt the script.

---

## Disclaimer

This tool modifies a system file (`hosts`). It is provided as-is, with no warranty. Use it at your own risk. The author is not affiliated with Roblox Corporation and takes no responsibility for any consequences of using this software.

---

## License

MIT License.
