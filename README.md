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
  "Country": "united states",
  "State": "georgia",
  "AdministrativeArea": "douglas county",
  "name": "Woods Valley",
  "id": "4231869"
}
```

### Example config file

```json
{
  "dictionary": {
    "id_attribute": "id",
    "value_attribute": [
      "name"
    ]
  },
  "document": {
    "id_attribute": "id",
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
                        a json file contains fields, tokensize and threshold

## Output
```json
{
  "entities": {
    "4231869": {
      "value": "Woods Valley",
      "candwins": [
        {
          "start": 64,
          "score": 11,
          "end": 74
        },
        {
          "start": 65,
          "score": 10,
          "end": 74
        },
        {
          "start": 196,
          "score": 10,
          "end": 206
        }
      ]
    }
  },
  "document": {
    "id": "4231868",
    "value": "The choice of San Diego golf enthusiasts and beginners alike is Woods Valley Golf Club. Stunning tree-lined fairways and beautiful rolling slopes highlight the 18-hole championship golf course at Woods Valley. Designed with an emphasis on strategy and shot-making, the course winds through the community, following the natural contours of the countryside."
  }
}
```
