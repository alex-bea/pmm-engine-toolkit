# Third-Party Notices

## Distribution contents

This source distribution does not vendor third-party source code, binaries, fonts,
images, screenshots, recordings, documents, or datasets. The root `LICENSE` file is the
official Apache License 2.0 text used as this project's licensing instrument.

## Runtime dependencies

The following packages are named in `requirements.txt` and are installed separately by
the user. They are not redistributed in this repository. The versions below are the
versions inspected during the 2026-08-18 rights review; each installed distribution
declared the MIT license.

| Dependency | Declared constraint | Inspected version | Upstream |
| --- | --- | --- | --- |
| PyYAML | `>=6.0` | 6.0.3 | [yaml/pyyaml](https://github.com/yaml/pyyaml) |
| Radon | `>=6.0` | 6.0.1 | [rubik/radon](https://github.com/rubik/radon) |
| cognitive-complexity | `>=1.3` | 1.3.0 | [Melevir/cognitive_complexity](https://github.com/Melevir/cognitive_complexity) |

Users receive those packages under their upstream license terms. Any future release that
vendors dependency code or binaries must add the applicable copyright and license notices
before distribution.

CI also installs the following hash-locked build tools separately; they are not vendored:

| Build tool | Inspected version | Declared license expression |
| --- | --- | --- |
| packaging | 26.3 | Apache-2.0 OR BSD-2-Clause |
| setuptools | 84.0.0 | MIT |
| wheel | 0.48.0 | MIT |

## Names and trademarks

Git, GitHub, OpenAI, LinkedIn, Slack, PyYAML, Radon, cognitive-complexity, and other product
or service names may be trademarks of their respective owners. This project uses those
names nominatively to identify a tool, format, integration boundary, or intended workflow.
It is not affiliated with or endorsed by those owners.

External hyperlinks identify public reference material only; linked content is not copied
into or licensed as part of this repository.
