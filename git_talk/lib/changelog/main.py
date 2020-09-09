


import os
import logging
from typing import Optional

import click

from git_talk.lib.changelog import generate_changelog
from git_talk.lib.changelog.presenter import MarkdownPresenter
from git_talk.lib.changelog.repository import GitRepository


# @click.command()
# @click.option(
#     "-r",
#     "--repo",
#     type=click.Path(exists=True),
#     default=".",
#     help="Path to the repository's root directory [Default: .]",
# )
# @click.option("-t", "--title", default="Changelog", help="The changelog's title [Default: Changelog]")
# @click.option("-d", "--description", help="Your project's description")
# @click.option(
#     "-o",
#     "--output",
#     type=click.File("w"),
#     default="CHANGELOG.md",
#     help="The place to save the generated changelog [Default: CHANGELOG.md]",
# )
# @click.option("-r", "--remote", default="origin", help="Specify git remote to use for links")
# @click.option("-v", "--latest-version", type=str, help="use specified version as latest release")
# @click.option("-u", "--unreleased", is_flag=True, default=False, help="Include section for unreleased changes")
# @click.option("--diff-url", default=None, help="override url for compares, use {current} and {previous} for tags")
# @click.option("--issue-url", default=None, help="Override url for issues, use {id} for issue id")
# @click.option(
#     "--issue-pattern",
#     default=r"(#([\w-]+))",
#     help="Override regex pattern for issues in commit messages. Should contain two groups, original match and ID used "
#     "by issue-url.",
# )
# @click.option(
#     "--tag-pattern",
#     default=None,
#     help="override regex pattern for release tags. "
#     "By default use semver tag names semantic. "
#     "tag should be contain in one group named 'version'.",
# )
# @click.option("--tag-prefix", default="", help='prefix used in version tags, default: "" ')
# @click.option("--stdout", is_flag=True)
# @click.option("--tag-pattern", default=None, help="Override regex pattern for release tags")
# @click.option("--starting-commit", help="Starting commit to use for changelog generation", default="")
# @click.option("--stopping-commit", help="Stopping commit to use for changelog generation", default="HEAD")
# @click.option(
#     "--debug", is_flag=True, help="set logging level to DEBUG",
# )
def main(
    repo,
    description,
    latest_version,
    title="Changelog",
    output="CHANGELOG.md",
    remote ="origin",
    unreleased=False,
    diff_url=None,
    issue_url=r"(#([\w-]+))",
    issue_pattern=None,
    tag_prefix="",
    stdout=True,
    tag_pattern=None,
    starting_commit="",
    stopping_commit ="HEAD",
    debug = False
):
    if debug:
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Logging level has been set to DEBUG")

    # Convert the repository name to an absolute path
    repo = os.path.abspath(repo)

    repository = GitRepository(
        repo,
        latest_version=latest_version,
        skip_unreleased=not unreleased,
        tag_prefix=tag_prefix,
        tag_pattern=tag_pattern,
    )
    presenter = MarkdownPresenter()
    changelog = generate_changelog(
        repository,
        presenter,
        title,
        description,
        remote=remote,
        issue_pattern=issue_pattern,
        issue_url=issue_url,
        diff_url=diff_url,
        starting_commit=starting_commit,
        stopping_commit=stopping_commit,
    )

    # if stdout:
    #     print(changelog)
    # else:
    #     output.write(changelog)
    changelog_file = os.path.join(repo, "CHANGELOG.md")
    write_changelog(changelog_file, changelog)

def write_changelog(changelog_file, changelog):
    if os.path.exists(changelog_file):
        with open(changelog_file, 'r') as f:
            data = f.read()
        with open(changelog_file, 'w') as f:
            # f.write(changelog + '\n\n' + data)
            f.write(changelog)
    else:
        with open(changelog_file, 'w') as f:
            f.write(changelog)

if __name__ == "__main__":
    main()