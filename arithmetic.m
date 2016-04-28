
% clear classes, scripts, etc
clear classes;

% Import module
mod = py.importlib.import_module('arithmetic');

% Some source and code example
source_code = 'arithmetic';
code = 0.0757451536000

% Setup the probabilities and the rage for each symbol
probabilities = py.arithmetic.set_probability(source_code);
symbols_with_range = py.arithmetic.set_range(probabilities);

% Encoding
result = py.arithmetic.encode(source_code, probabilities);

% Decoding
result = py.arithmetic.encode(code, probabilities);