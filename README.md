# Web Data Extractor

Tool to extract tabular data from files on the web.

Supports fetching data through HTTP or FTP.

## Configuration

A config.json file is required to run the extractor.
Multiple configurations may be included in the config file in the following form:

```json
[
    {
        // configuration...
    },
    // ...
]
```

### Required Options

#### `title`
The title of the configuration.
```
"title": "Sample Title"
```
#### `url` or `host`
The url (_http_) or host (_ftp_) of the configuration.

__For http__: use whole path together with file name and extension.

```
"url": "http://www.example.com/example.csv"
```

__For ftp__: use only hostname, without file name and extension. File name provided in seperate option.
```
"host": "192.168.0.1"
```
