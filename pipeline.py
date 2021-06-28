import argparse
from pathlib import Path

import markdown
from alert_extension import AlertExtension

DOCUMENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
</head>
<body>
    <div class="container">
        {text}
    </div>
</body>
</html>
"""


def main(source: Path, destination: Path) -> None:
    extensions = [AlertExtension()]
    md = markdown.Markdown(extensions=extensions)

    with open(source) as f:
        text = f.read()

    html = md.convert(text)
    result = DOCUMENT.format(text=html)

    with open(destination, "w") as f:
        f.write(result)


def get_parser() -> argparse.ArgumentParser:
    _parser = argparse.ArgumentParser(description="Markdown Concersion Pipeline CLI")
    _parser.add_argument(
        "source",
        type=Path,
        help="The path to the source file",
    )
    _parser.add_argument(
        "destination",
        type=Path,
        help="The path to the destination file",
    )

    return _parser


if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    main(args.source, args.destination)
