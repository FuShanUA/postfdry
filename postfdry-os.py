"""
postfdry-os.py

The main orchestrator for the 7-Agent Postfdry virtual editorial team.
This script provides a unified CLI to trigger individual agents.

Usage:
  python postfdry-os.py --agent <name> [args...]
"""

import sys
import os
import subprocess

AGENTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "agents")

AGENTS = {
    "crawler": "crawler_agent.py",
    "translator": "translator_agent.py",
    "rewriter": "rewriter_agent.py",
    "cover": "cover_illustrator.py",
    "infographic": "infographic_illustrator.py",
    "pdf": "pdf_publisher.py",
    "wechat": "wechat_publisher.py",
    "patcher": "patcher_agent.py",
    "editor": "editor_agent.py"
}

def print_help():
    print("Postfdry-OS Editorial Team Orchestrator")
    print("Usage: python postfdry-os.py --agent <name> [args...]")
    print("\nAvailable Agents:")
    for name, script in AGENTS.items():
        print(f"  {name:<12} -> calls agents/{script}")

def run_agent(agent_name, args):
    if agent_name not in AGENTS:
        print(f"Error: Unknown agent '{agent_name}'")
        print_help()
        sys.exit(1)
        
    script_path = os.path.join(AGENTS_DIR, AGENTS[agent_name])
    if not os.path.exists(script_path):
        print(f"Error: Script not found -> {script_path}")
        sys.exit(1)
        
    cmd = [sys.executable, script_path] + args
    print(f"\n[Orchestrator] Dispatching to {agent_name.upper()} Agent...")
    print(f"[Orchestrator] Command: {' '.join(cmd)}\n")
    
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"\n[Orchestrator] Agent {agent_name.upper()} returned an error: {e}")
        sys.exit(e.returncode)

if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[1] != "--agent":
        print_help()
        sys.exit(1)
        
    agent = sys.argv[2]
    agent_args = sys.argv[3:]
    run_agent(agent, agent_args)
