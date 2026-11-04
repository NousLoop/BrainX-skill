"""Retrieve official API pages, without inspecting installed library internals."""
import hashlib
import html.parser
import json
from pathlib import Path
import urllib.request


class Text(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
    def handle_data(self, value):
        if value.strip():
            self.parts.append(value.strip())


root = Path(__file__).parent / 'outer-audit' / 'official-api'
root.mkdir(parents=True, exist_ok=True)
urls = {
    'WilsonCowanStep': 'brainmass/reference/generated/brainmass.WilsonCowanStep.html',
    'Simulator': 'brainmass/reference/generated/brainmass.Simulator.html',
    'forward': 'brainmass/reference/forward.html',
    'activation': 'brainstate/apis/nn/activation.html',
    'Constant': 'braintools/apis/generated/braintools.init.Constant.html',
    'Sinusoidal': 'braintools/apis/generated/braintools.input.Sinusoidal.html',
    'spectral': 'braintools/apis/metric.html',
    'PSD': 'braintools/apis/generated/braintools.analysis.spectral.power_spectral_density.html',
    'PAC': 'braintools/apis/generated/braintools.analysis.spectral.phase_amplitude_coupling.html',
    'bandpass': 'braintools/apis/generated/braintools.analysis.spectral.bandpass.html',
    'analytic_signal': 'braintools/apis/generated/braintools.analysis.spectral.analytic_signal.html',
    'sigmoid': 'brainstate/apis/generated/brainstate.nn.sigmoid.html',
    'Quantity': 'brainunit/apis/generated/brainunit.Quantity.html',
    'viz': 'brainmass/reference/viz.html',
    'environ': 'brainstate/apis/environ.html',
}
receipt = {}
for name, route in urls.items():
    url = 'https://brainx.chaobrain.com/' + route
    try:
        raw = urllib.request.urlopen(url, timeout=30).read()
        parser = Text()
        parser.feed(raw.decode())
        (root / (name + '.txt')).write_text(url + '\n' + '\n'.join(parser.parts), encoding='utf-8')
        receipt[name] = {'url': url, 'sha256_html': hashlib.sha256(raw).hexdigest(), 'status': 'retrieved'}
    except Exception as exc:
        receipt[name] = {'url': url, 'status': 'failed', 'error': str(exc)}
(root / 'receipt.json').write_text(json.dumps(receipt, indent=2))
print(json.dumps(receipt, indent=2))
