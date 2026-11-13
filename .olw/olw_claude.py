"""Run olw against Claude through Anthropic's OpenAI-compatible endpoint.

olw's OpenAI-compatible client checks the connection with GET {base_url}/models.
On api.anthropic.com that call needs an `anthropic-version` header, which olw never
sends, so `olw doctor` and `olw query` report "Cannot reach custom". This wrapper
adds the header in memory and then runs the normal olw CLI. The installed package
is not modified.

Usage (from the vault root), with the same arguments as `olw`:
    python .olw/olw_claude.py query "คำถาม"
    python .olw/olw_claude.py doctor
"""
from obsidian_llm_wiki import openai_compat_client as occ
from obsidian_llm_wiki.cli import cli

_orig_build_headers = occ.OpenAICompatClient._build_headers


def _build_headers(self):
    headers = dict(_orig_build_headers(self))
    if "api.anthropic.com" in self.base_url:
        headers["anthropic-version"] = "2023-06-01"
    return headers


occ.OpenAICompatClient._build_headers = _build_headers

if __name__ == "__main__":
    cli(prog_name="olw")
