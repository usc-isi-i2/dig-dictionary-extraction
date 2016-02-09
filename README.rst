===================
entity_extraction
===================

This is an implementation of faeire entity extraction, a dictionary-baesd entity extraction.

---------------------
For install:
---------------------

pre-request:

you need to install nltk and its data:

1.run 
::
	sudo pip install -U nltk to install nltk

2.run python and type these commands:
::
	>>> import nltk
	>>> nltk.download()

3.run 
::
	sudo pip install faerie

--------------------
Usage:
--------------------

Input format for both dictionary and documents:

{"rdfs:label": "http://schema.org/City", "name": "Los Angeles", "additionalProperty": {"value": "0", "a": "PropertyValue", "text": "Population"}, "@context": "http://localhost:8080/publish/JSON/WSP9WS1-allcountries_sample_txt-context.json", "containedIn": {"AdministrativeArea": "la salle county", "State": "texas", "Country": "united states"}, "sameAs": "http://www.geonames.org/4046384", "geo": {"longitude": "-99.00003", "latitude": "28.46582", "a": "GeoCoordinates"}, "additionalType": "http://dig.isi.edu/gazetteer/geonames/Placetype/P_PPL", "alternateName": "Los Angeles", "uri": "http://dig.isi.edu/gazetteer/geonames/4046384", "a": "City"}

run 
::
	faerie.run(dictionary,documents,dictfiledsarray,docfiledsarray,ngram(optional),threshold(optional)) 
to run the entity extraction. 

-------------------------------------
Current output is a json line:
-------------------------------------

{"entities": {"4046384": {"value": "Los Angeles", "candwins": [{"start": 0, "score": 9, "end": 9}]}, "4505286": {"value": "Angel", "candwins": [{"start": 4, "score": 3, "end": 7}]}, "4830172": {"value": "Angel", "candwins": [{"start": 4, "score": 3, "end": 7}]}, "4984229": {"value": "Angel", "candwins": [{"start": 4, "score": 3, "end": 7}]}, "5516301": {"value": "Angeles", "candwins": [{"start": 4, "score": 5, "end": 9}]}, "4707891": {"value": "Los Angeles", "candwins": [{"start": 0, "score": 9, "end": 9}]}}, "document": {"id": "4046384", "value": "Los Angeles"}}
