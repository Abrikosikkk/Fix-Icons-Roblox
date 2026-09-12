# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import ctypes
import re
from pathlib import Path

DOMAIN = "tr.rbxcdn.com"
HOSTS_PATH = Path(os.environ.get("SystemRoot", "C:\\Windows")) / "System32" / "drivers" / "etc" / "hosts"
DNS_SERVERS = ["9.9.9.9", "1.1.1.1"]


def is_admin() -> bool:
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def elevate():
    script = os.path.abspath(sys.argv[0])
    params = " ".join(f'"{a}"' for a in sys.argv[1:])
    try:
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, f'"{script}" {params}', None, 1
        )
    except Exception as e:
        print(f"  ✗ Не удалось повысить привилегии: {e}")
    sys.exit(0)


def resolve_ip(domain: str, dns_server: str):
    try:
        proc = subprocess.run(
            ["nslookup", domain, dns_server],
            capture_output=True, text=True, timeout=10,
            creationflags=subprocess.CREATE_NO_WINDOW,
        )
        output = f"{proc.stdout}\n{proc.stderr}"
        ips = re.findall(r"Address(?:es)?:\s+([\d.]+)", output)
        candidates = [ip for ip in ips if ip != dns_server and not ip.startswith("127.")]
        return candidates[0] if candidates else None
    except subprocess.TimeoutExpired:
        return None
    except Exception:
        return None


def load_hosts() -> str:
    if not HOSTS_PATH.exists():
        return ""
    try:
        return HOSTS_PATH.read_text(encoding="utf-8", errors="ignore")
    except OSError as e:
        print(f"  ✗ Чтение hosts провалилось: {e}")
        return ""


def patch_hosts(ip: str, domain: str) -> bool:
    lines = load_hosts().splitlines()
    kept, dropped = [], 0

    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            kept.append(line)
            continue
        if domain in stripped:
            dropped += 1
            continue
        kept.append(line)

    if kept and kept[-1].strip():
        kept.append("")
    kept.append(f"{ip} {domain}")

    try:
        HOSTS_PATH.write_text("\n".join(kept) + "\n", encoding="utf-8")
        print(f"  ✓ hosts пропатчен → {ip} {domain}")
        if dropped:
            print(f"    ↳ вычищено устаревших записей: {dropped}")
        return True
    except PermissionError:
        print("  ✗ Нет прав на запись в hosts. Запусти от имени администратора.")
        return False
    except OSError as e:
        print(f"  ✗ Запись hosts провалилась: {e}")
        return False


def flush_dns() -> None:
    print("  · сброс DNS-кэша…")
    subprocess.run(
        ["ipconfig", "/flushdns"],
        capture_output=True, text=True,
        creationflags=subprocess.CREATE_NO_WINDOW,
    )
    print("  ✓ DNS-кэш очищен")


def banner() -> None:
    print()
    print("  ┌─────────────────────────────────────────────┐")
    print("  │  fix_iconsroblox.py                         │")
    print("  │  Roblox CDN Resolver · v1.0                 │")
    print("  └─────────────────────────────────────────────┘")
    print()


def main() -> None:
    banner()

    if os.name != "nt":
        print("  ✗ Скрипт рассчитан на Windows.")
        return

    if not is_admin():
        print("  · прав недостаточно — перезапуск с UAC…")
        elevate()
        return

    print(f"  · target  : {DOMAIN}")
    print(f"  · hosts   : {HOSTS_PATH}")
    print(f"  · dns     : {', '.join(DNS_SERVERS)}")
    print()

    print("  [1/3] Резолвим актуальный IP…")
    resolved = None
    for dns in DNS_SERVERS:
        print(f"        → запрос через {dns}")
        ip = resolve_ip(DOMAIN, dns)
        if ip:
            print(f"        ✓ ответ: {ip}")
            resolved = ip
            break
        print("        ✗ ответа нет")

    if not resolved:
        print()
        print("  ✗ Не удалось получить IP ни от одного резолвера.")
        print("    Варианты: смени DNS на 9.9.9.9 или используй VPN.")
        print()
        input("  Нажми Enter для выхода…")
        return

    print()
    print("  [2/3] Обновляем системный hosts…")
    if not patch_hosts(resolved, DOMAIN):
        print()
        input("  Нажми Enter для выхода…")
        return

    print()
    print("  [3/3] Сбрасываем кэш…")
    flush_dns()

    print()
    print("  ─────────────────────────────────────────────")
    print("  ✓ Готово. Перезапусти Roblox.")
    print("  ─────────────────────────────────────────────")
    print()
    input("  Нажми Enter для выхода…")


if __name__ == "__main__":
    main()