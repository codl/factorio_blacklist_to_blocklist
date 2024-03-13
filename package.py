import json
import argparse
from pathlib import Path
import subprocess


class InfoJsonError(Exception):
    pass


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=Path, default="./blacklist_to_blocklist")
    parser.add_argument("-o", "--output", type=Path, default="./dist")
    args = parser.parse_args()

    directory: Path = args.input
    outdir: Path = args.output

    if not directory.exists():
        raise FileNotFoundError("{} does not exist".format(directory))

    if not outdir.exists():
        outdir.mkdir(parents=True)

    infojson = directory / "info.json"

    if not infojson.exists():
        raise FileNotFoundError("{} does not exist".format(infojson))

    info = json.loads(infojson.read_text())

    if "name" not in info or "version" not in info:
        raise InfoJsonError(
            "{} does not contain the required keys (name, version)".format(infojson)
        )

    outfile = outdir / ("{}_{}.zip".format(info["name"], info["version"]))
    if outfile.exists:
        outfile.unlink()

    subprocess.run(
        ("zip", "--quiet", "--recurse-paths", outfile, directory.relative_to(directory.parent)),
        cwd=directory.parent,
    )

    print("Packaged to {}".format(outfile))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        exit(1)
