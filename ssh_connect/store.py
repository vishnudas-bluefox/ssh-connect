from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


CONFIG_DIR = Path(os.environ.get("SSH_CONNECT_CONFIG_DIR", Path.home() / ".config" / "ssh-connect"))
CONFIG_FILE = CONFIG_DIR / "connections.json"


@dataclass
class Connection:
    name: str
    host: str
    user: str = "ubuntu"
    pem_file: str = ""
    port: int = 22
    extra_args: list[str] | None = None

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        if not data["extra_args"]:
            data.pop("extra_args", None)
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Connection:
        return cls(
            name=data["name"],
            host=data["host"],
            user=data.get("user", "ubuntu"),
            pem_file=data.get("pem_file", ""),
            port=int(data.get("port", 22)),
            extra_args=data.get("extra_args"),
        )

    def resolved_pem(self) -> Path | None:
        if not self.pem_file:
            return None
        return Path(self.pem_file).expanduser().resolve()

    def ssh_command(self) -> list[str]:
        cmd = ["ssh"]
        pem = self.resolved_pem()
        if pem:
            cmd.extend(["-i", str(pem)])
        if self.port != 22:
            cmd.extend(["-p", str(self.port)])
        if self.extra_args:
            cmd.extend(self.extra_args)
        cmd.append(f"{self.user}@{self.host}")
        return cmd


def _ensure_config() -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if not CONFIG_FILE.exists():
        CONFIG_FILE.write_text("{}\n", encoding="utf-8")


def load_all() -> dict[str, Connection]:
    _ensure_config()
    raw = json.loads(CONFIG_FILE.read_text(encoding="utf-8") or "{}")
    return {name: Connection.from_dict({**data, "name": name}) for name, data in raw.items()}


def save_all(connections: dict[str, Connection]) -> None:
    _ensure_config()
    payload = {name: conn.to_dict() for name, conn in sorted(connections.items())}
    CONFIG_FILE.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def get(name: str) -> Connection | None:
    return load_all().get(name)


def add(connection: Connection) -> None:
    connections = load_all()
    connections[connection.name] = connection
    save_all(connections)


def delete(name: str) -> bool:
    connections = load_all()
    if name not in connections:
        return False
    del connections[name]
    save_all(connections)
    return True


def list_names() -> list[str]:
    return sorted(load_all().keys())
