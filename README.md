# ping-stats 

ping-stats is a `tool` that allows `you, the consumer` to monitor ping times, packet loss, and round-trip times from all IP Addresses in a trace.

Track and monitor all IP Addresses in a traceroute from point A to point B by gathering statistics about ping times measured in ms, packet loss measured in percentage, and round-trip times measured in ms. Dump all of this data, by IP Address, to a Prometheus formatted text file for collection by the Node Exporter service and the Prometheus server. Import this into Grafana for visual reporting.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.10.12+
- [mtr](https://thelinuxcode.com/mtr-a-diagnostic-tool/)
- If you want to collect this data, [Prometheus](https://prometheus.io/docs/introduction/overview/)
- If you want to visualize the data you collect, [Grafana](https://grafana.com/)

## Installing

To install ping-stats, follow these steps:

1. Check out the repository on a machine with `mtr` and `Python 3.10.12+` installed:
`git clone https://github.com/benowe1717/ping-stats.git`

2. Create a python virtual environment:
`python3.10 -m venv .venv`

If your default version is already on python 3.10+:
`python3 -m venv .venv`

3. Activate the newly created virtual environment:
`source .venv/bin/activate`

4. Install any required dependencies:
`python3 -m pip install -r requirements.txt`

If the `mtr` application is not installed, follow the steps from the Prerequisites section.

For more information on virtual environments, see below:
- https://docs.python.org/3/library/venv.html
- https://www.pythonguis.com/tutorials/python-virtual-environments/

## Using

To use ping-stats, follow these steps:

1. Edit the default configuration file, or, copy the default configuration file to another location and modify:
Default Location: `./src/configs/config.yaml`
Update the `prometheus` section with the appropriate filepaths to where you want the prometheus-formatted file to be stored

NOTE: The `temp_filename` key is optional, only if you want that filename to be different. Otherwise, it will use the same name as the `filename` key.

Update the `mtr` section with the IPs you want to monitor.

NOTE: Each IP should be on a separate line

2. Once your configuration file is created, simply run:
`python3 main.py --config-file /path/to/config.yaml`

## Contributing to ping-stats

To contribute to <project_name>, follow these steps:

1. Fork this repository
2. Create a branch: `git checkout -b <branch_name>`
3. Make your changes and commit them: `git commit -m '<commit_message>'`
4. Push to the original branch: `git push origin <project_name>/<location>`
5. Create the Pull Request

Alternatively see the GitHub documentation on [creating a pull request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).

## Contributors

Thanks to the following people who have contributed to this project:

- [@benowe1717](https://github.com/benowe1717)

## Contact

For help or support on this repository, follow these steps:

- [Create an issue](https://github.com/benowe1717/ping-stats/issues)

## License

This project uses the following license: GNU GPLv3.

## Sources

- https://github.com/scottydocs/README-template.md/blob/master/README.md
- https://choosealicense.com/
- https://www.freecodecamp.org/news/how-to-write-a-good-readme-file/
