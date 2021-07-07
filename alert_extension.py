import re
from textwrap import dedent

from markdown import Extension
from markdown.preprocessors import Preprocessor

SNIPPET = '''<div class="alert alert-{level}" role="alert">
<h4 class="alert-heading"><strong>{heading}</strong></h4>
{alert}
</div>'''

HEADINGS = {
    "primary": "",
    "secondary": "Note",
    "success": "Congratulations!",
    "danger": "Caution!",
    "warning": "Warning",
    "info": "Info",
    "light": "Note",
    "dark": "Note",
}


class AlertExtension(Extension):
    def __init__(self, **kwargs):
        self.config = {}
        super().__init__(**kwargs)

    def extendMarkdown(self, md):
        md.registerExtension(self)
        md.preprocessors.register(
            AlertBlockProcessor(md, self.getConfigs()
        ), 'alert_block', 25)


class AlertBlockProcessor(Preprocessor):
    ALERT_BLOCK_RE = re.compile(
        dedent(r'''
            :: (?P<level>[^\[\s+]+)( heading=["'](?P<heading>[^"']+)["'])?
            (?P<alert>[\s\S]*?)
            ::
        '''),
    )

    def __init__(self, md, config):
        super().__init__(md)
        self.config = config

    def run(self, lines):
        text = "\n".join(lines)
        while 1:
            m = self.ALERT_BLOCK_RE.search(text)
            if m:
                level = 'debug'
                if m.group('level'):
                    level = m.group('level')
                heading = HEADINGS.get(level, "Note")
                if m.group("heading"):
                    heading = m.group("heading")

                alert = self.md.convert(m.group("alert"))
                snippet = SNIPPET.format(level=level, alert=alert, heading=heading)
                placeholder = self.md.htmlStash.store(snippet)
                text = '{}\n{}\n{}'.format(
                    text[:m.start()],
                    placeholder,
                    text[m.end():],
                )
            else:
                break
        return text.split("\n")


def makeExtension(**kwargs):  # pragma: no cover
    return AlertExtension(**kwargs)
