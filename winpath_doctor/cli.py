import argparse
import os
import sys
from winpath_doctor.analyzer import PathAnalyzer
from winpath_doctor.backup import PathBackup


def main():
    parser = argparse.ArgumentParser(
        description="WinPath Doctor: Analyze, clean, and backup Windows PATH environment variable."
    )
    parser.add_argument(
        "--path",
        type=str,
        help="Custom PATH string to analyze instead of current environment PATH",
    )
    parser.add_argument("--clean", action="store_true", help="Output cleaned PATH string")
    parser.add_argument("--backup", action="store_true", help="Save a snapshot backup of current PATH")
    parser.add_argument("--list-backups", action="store_true", help="List all saved PATH backups")
    parser.add_argument(
        "--export-ps",
        action="store_true",
        help="Export cleaned PATH as PowerShell setting command",
    )

    args = parser.parse_args()
    path_str = args.path if args.path is not None else os.environ.get("PATH", "")

    if args.backup:
        mgr = PathBackup()
        saved_file = mgr.create_backup(path_str)
        print(f"Backup saved: {saved_file}")
        return

    if args.list_backups:
        mgr = PathBackup()
        backups = mgr.list_backups()
        if not backups:
            print("No backups found.")
            return
        for b in backups:
            print(f"[{b.get('timestamp')}] {b.get('filepath')} ({len(b.get('entries', []))} entries)")
        return

    analyzer = PathAnalyzer(path_str)
    report = analyzer.generate_report()

    if args.export_ps:
        clean_str = report["cleaned_path_str"]
        print(f'$env:Path = "{clean_str}"')
        return

    if args.clean:
        print(report["cleaned_path_str"])
        return

    print("=== WinPath Doctor Analysis Report ===")
    print(f"Total Entries : {report['total_entries']}")
    print(f"Duplicates    : {report['duplicate_count']}")
    print(f"Dead Paths    : {report['dead_count']}")
    print()

    if report["duplicates"]:
        print("--- Duplicates Found ---")
        for idx, raw in report["duplicates"]:
            print(f"  [{idx}] {raw}")
        print()

    if report["dead_paths"]:
        print("--- Dead or Invalid Directories ---")
        for idx, raw in report["dead_paths"]:
            print(f"  [{idx}] {raw}")
        print()

    print("Use --clean to print optimized PATH or --backup to create snapshot.")


if __name__ == "__main__":
    main()
