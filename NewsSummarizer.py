# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *
import typing


class NewsSummarizer(gl.Contract):
    last_summary: str

    def __init__(self):
        self.last_summary = "No summary yet"

    @gl.public.write
    def fetch_news(self) -> typing.Any:
        def get_news() -> str:
            response = gl.nondet.web.get("https://feeds.bbci.co.uk/news/rss.xml")
            data = response.body.decode("utf-8")[:3000]
            result = gl.nondet.exec_prompt(
                f"From this BBC RSS feed, extract the first headline and summarize it in one sentence in English. Return only the summary, nothing else: {data}"
            )
            return result.strip()

        def validate(leader_result) -> bool:
            if not isinstance(leader_result, gl.vm.Return):
                return False
            return isinstance(leader_result.calldata, str) and len(leader_result.calldata) > 0

        self.last_summary = gl.vm.run_nondet_unsafe(get_news, validate)

    @gl.public.view
    def show_summary(self) -> str:
        return self.last_summary
