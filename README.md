# Team Dinasaurs Large Group project

## Team members
The members of the team are:
- Dilara Mukasheva 
- Anahita Savarypour
- Dina Ghazaani
- Lara Ergenc
- Maryam Marei 
- Jiaxuan (Emilie) Yu

## Project structure
The project is called `Universal Student society Webpages`.  It currently consists of a single app `Hive Society`.

## Deployed version of the application
The deployed version of the application can be found at [https://hivesociety.vercel.app].

## Installation instructions
To install the software and use it in your local development environment, you must first set up and activate a local development environment.  From the root of the project:

```
$ virtualenv venv
$ source venv/bin/activate
```

Install all required packages:

```

$ pip3 install -r requirements.txt

```

Migrate the database:

```
$ python3 manage.py migrate
```

Seed the development database with:

```
$ python3 manage.py seed
```

Run all tests with:
```
$ python3 manage.py test
```


## Sources
The packages used by this application are specified in `requirements.txt`


