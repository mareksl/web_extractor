# Web Data Extractor

- [Web Data Extractor](#web-data-extractor)
  - [Configuration](#configuration)
    - [Required Settings](#required-settings)
      - [`title`](#title)
      - [`url` or `host`](#url-or-host)
      - [`filename` (FTP)](#filename-ftp)
    - [Optional Settings](#optional-settings)
      - [`dateFormat`](#dateformat)
      - [`authentication`](#authentication)
 

Tool to extract tabular data from files on the web.

Supports fetching data through HTTP or FTP.


## Configuration

A config.json file is required to run the extractor.
Multiple configurations may be included in the config file in the following form:

```
[
    {
        // configuration...
    },
    // ...
]
```

### Required Settings


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

You can provide a placeholder for the current date in the url between curly braces. This will be replaced by today's date in the format you specify in the [`dateFormat`](#dateFormat) option:

```
"url": "http://www.example.com/file_from_today_{date}.csv"
```

__For ftp__: use only hostname, without file name and extension. [Filename](#filename-(FTP)) provided in seperate option.

```
"host": "192.168.0.1"
```


#### `filename` (FTP)

When using the FTP protocol, the name of the file to be extracted is also required:

```
"filename": "example.csv"
```


### Optional Settings


#### `dateFormat`

Format of the date to be embedded in url (HTTP only). `dateFormat` has to be provided using Python's `strftime` directives. [Refer to this list of available directives.](http://strftime.org/)

```
"dateFormat": "%Y%m%d"
```

In this example, the date 25. March 2019 will be formatted as: _20190328_.


#### `authentication`
