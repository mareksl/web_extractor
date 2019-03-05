# Web Data Extractor

- [Web Data Extractor](#web-data-extractor)
  - [Running the program](#running-the-program)
  - [Configuration](#configuration)
    - [Required Settings](#required-settings)
      - [`title`](#title)
      - [`url` or `host`](#url-or-host)
      - [`filename` (FTP)](#filename-ftp)
    - [Optional Settings](#optional-settings)
      - [`dateFormat`](#dateformat)
      - [`authentication`](#authentication)
      - [`encoding`](#encoding)
      - [`separator`](#separator)
      - [`filters`](#filters)
      - [`columns`](#columns)
      - [`aliases`](#aliases)
  - [License](#license)
 

Tool for extracting tabular data from files on the web.

Supports fetching data through __HTTP__ or __FTP__.

The program processes the data from the file provided in the configuration, filters it by a given column, extracts only the required columns provided in the configuration and outputs a csv file with the extracted data to the output folder.

## Running the program

1. Provide a configuration in the _config.json_ file. Refer to the [configuration](#configuration) section for information on how to configure the program.
2. Run the executable.
3. Use the arrows to choose the action.
4. Result can be found in the _./output_ folder.


## Configuration

A config.json file is required to run the extractor.
Multiple configurations may be included in the config file in the following form:

```
[
    {
        "title": "Example configuration",
        "url": "http://www.example.com",
        // ...
    },
    // ...
]
```

Full list of available configuration options below.


### Required Settings

This is the minimal information that has to be provided in order for the program to work. Depending on the source of the data, youmay have to provide [authentication](#authentication) and/or [encoding](#encoding) details.

#### `title`

The title of the configuration.

Example:
```
"title": "Sample Title"
```


#### `url` or `host`

The url (_http_) or host (_ftp_) of the configuration.

__For http__: use whole path together with file name and extension.

Example:
```
"url": "http://www.example.com/example.csv"
```

You can provide a placeholder for the current date in the url between curly braces. This will be replaced by today's date in the format you specify in the [`dateFormat`](#dateFormat) option.

Example:
```
"url": "http://www.example.com/file_from_today_{date}.csv"
```

__For ftp__: use only hostname, without file name and extension. [Filename](#filename-(FTP)) provided in seperate option.

Example:
```
"host": "192.168.0.1"
```


#### `filename` (FTP)

When using the FTP protocol, the name of the file to be extracted is also required.

Example:
```
"filename": "example.csv"
```


### Optional Settings

These setitngs are optional, but [authentication](#authentication) and/or [encoding](#encoding) details may have to be provided for certain sources.

#### `dateFormat`

Format of the date to be embedded in url (HTTP only). `dateFormat` has to be provided using Python's `strftime` directives. [Refer to this list of available directives.](http://strftime.org/)

Example:
```
"dateFormat": "%Y%m%d"
```

In this example, the date 25. March 2019 will be formatted as: _20190328_.


#### `authentication`

Basic authentication details including `username` and `password`.

Example:
```
"authentication": {
    "username": "exampleUser",
    "password": "examplePassword"
}
```


#### `encoding`

The text encoding of the file to be extracted. Defaults to __`utf8`__.

Example:
```
"encoding": "iso-8859-1"
```


#### `separator`

The characted used as separator in the file. Use `\t` for tabs. Defaults to __`;`__.

Example:
```
"separator": "\t"
```


#### `filters`

The columns and values by which to filter in the form of an object with the name of the column as the key and a list of strings to filter by as value.

Example:
```
"filters": {
    "column1": [
        "value1",
        "value2"
    ],
    "column2": [
        "value1",
        "value2"
    ]
}
```


#### `columns`

A list of columns to be included in result. All columns will be included if left blank.

Example:
```
"columns": ["column1", "column3"]
```


#### `aliases`

A list of aliases for the included columns in their order. If no aliases provided, the columns will keep the names from the original file.

Example:
```
"aliases": ["renamedColumn1", "renamedColumn2"]
```

## License
[MIT](https:/github.com/mareksl/swx_tool/LICENSE)