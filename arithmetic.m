
% clear classes, scripts, etc
clear classes;

% Import module
% You can import the file inside src folder or the package installed
mod = py.importlib.import_module('arithmetic');


% Some source and code example
source_code = 'arithmetic';
code = 0.0757451536000;

% Setup the probabilities and the rage for each symbol
probabilities = py.arithmetic.set_probability(source_code);
symbols_with_range = py.arithmetic.set_range(probabilities);

% Encoding
encoded = py.arithmetic.encode(source_code, symbols_with_range)

% Decoding
decoded = py.arithmetic.decode(encoded, symbols_with_range)