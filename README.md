# Arithmetic Coding
Encode and decode a file using the arithmetic coding algorithm


### Install

```
    $ pip install -e .
```
  
### Using

Encoding a file:

```
    $ arithmetic <file> [options]
```

Decoding a file:

```
    $ arithmetic <file.table | file.acod> -d [options]
```
  
More options:

```
    $ arithmetic --help
```

### Installing MATLAB engine API for Python

You gonna need a MATLAB version R2014b or newer. 

- On Windows Systems

```
    cd "matlabroot\extern\engines\python"
    python setup.py install
```

- On Mac or Linux systems

```
    $ cd "matlabroot/extern/engines/python"
    # python setup.py install
```


Check [here](http://www.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html) for more info.

#### Using from MATLAB

Check the file [arithmetic.m](arithmetic.m) for a quick example.