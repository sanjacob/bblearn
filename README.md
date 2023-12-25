# Blackboard Learn API Client

> This project is not endorsed by Blackboard© but developed independently

Developed with [`tiny-api-client`][tiny-api-client]

This library started as part of [Blackboard Sync][bbsync], but decided it could be extracted into its own distribution package.

```python
from blackboard import BlackboardSession

session = BlackboardSession('http://blackboard.example.com/learn/api/public/v{version}', cookies=...)
session.fetch_version()
```


## Installation

```bash
pip install bblearn
```



## License

[![License: GPL  v2.1][license-shield]][gnu]

This software is distributed under the [General Public License v2][license], more information available at the [Free Software Foundation][gnu].


<!-- LINKS -->

[tiny-api-client]: https://pypi.org/project/tiny-api-client
[bbsync]: https://github.com/sanjacob/BlackboardSync


<!-- LICENSE -->

[license]: LICENSE "General Public License v2"
[gnu]: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html "Free Software Foundation"
[license-shield]: https://img.shields.io/github/license/sanjacob/bblearn


<!-- SHIELD LINKS -->

[pypi]: https://pypi.org/project/bblearn


<!-- SHIELDS -->

[pypi-shield]: https://img.shields.io/pypi/v/bblearn
[build-shield]: https://img.shields.io/github/actions/workflow/status/sanjacob/bblearn/build.yml?branch=master
[docs-shield]: https://img.shields.io/readthedocs/bblearn
