# Faerie Entity Extraction

This is an implementation of [faeire entity extraction](http://dbgroup.cs.tsinghua.edu.cn/ligl/papers/sigmod2011-faerie.pdf), a dictionary-baesd entity extraction.

## Installation and dependencies

```bash
pip install faerie
```

## Usage


```bash
faerie.run(dictionary,documents,config) 
```
### Example input and dictionary file

```json
{
  "name": "Los Angeles",
  "AdministrativeArea": "la salle county",
  "State": "texas",
  "Country": "united states",
  "uri": "http://dig.isi.edu/gazetteer/geonames/4046384",
}
```

### Example config file

```json
{
  "dictionary": {
    "id_attribute": "uri",
    "value_attribute": [
      "name"
    ]
  },
  "document": {
    "id_attribute": "uri",
    "value_attribute": [
      "name"
    ]
  },
  "token_size": 2,
  "threshold": 0.8
}
```

### Arguments:

#### Required

  * `documents` a json file for extracting entities

And
  * `dictionary` a json file providing entities to extract

#### Optional
  * `config`
                        json file contains fields, tokensize and threshold

## Output
```json
{
  "entities": {
    "4046384": {
      "value": "Los Angeles",
      "candwins": [
        {
          "start": 0,
          "score": 9,
          "end": 9
        }
      ]
    },
    "4505286": {
      "value": "Angel",
      "candwins": [
        {
          "start": 4,
          "score": 3,
          "end": 7
        }
      ]
    },
    "4830172": {
      "value": "Angel",
      "candwins": [
        {
          "start": 4,
          "score": 3,
          "end": 7
        }
      ]
    },
    "4984229": {
      "value": "Angel",
      "candwins": [
        {
          "start": 4,
          "score": 3,
          "end": 7
        }
      ]
    },
    "5516301": {
      "value": "Angeles",
      "candwins": [
        {
          "start": 4,
          "score": 5,
          "end": 9
        }
      ]
    },
    "4707891": {
      "value": "Los Angeles",
      "candwins": [
        {
          "start": 0,
          "score": 9,
          "end": 9
        }
      ]
    }
  },
  "document": {
    "id": "4046384",
    "value": "Los Angeles"
  }
}

```
