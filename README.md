Bazema linker
=============

Application building relations between drugs,
 scientific publications, pubmed, journals and
 clinical trials.

The output is a JSON file.

## Design
       +-------------------------+
       | input folder            |
       |   + drugs.csv           |
       |   | pubmed.csv          |
       |   | pubmed.json         |
       |   + clinical_trials.csv |
       +-------------------------+
                   +         move valid
                   |         files    +------------------+
                   v           +----> |  archive folder  |
          +--------+-------+   |      +------------------+
          |                |+--+
          | bazema_linker  |
          | python job     |     move invalid
          |                |±--+ files
          +----------------+   |      +------------------+
                   +           +----> |  errors folder   |
                   |                  +------------------+
                   v
    +-----------------------------+
    |  output folder              |
    |   + result_2020_10_06.json  |
    +-----------------------------+

Once the job is done, the input files are moved to an `archive`
folder. 
Invalid files (name invalid, format invalid, parsing impossible)
are moved to an `errors` folder.

## Structure of input files

- `drugs.csv`, 2 columns= `atccode` and`drug`
- `pubmed.csv`, 4 columns= `id`, `title`, `date` and `journal`
- `pubmed.json`, same structure as a JSON
- `clinical_trials.csv`, 4 columns= `id`, `scientific_title`, `date` and `journal`

## Structure of generated output
    [
        {
            "drug": "drug name",
            "clinical_trials": [
                {
                    "title": "title of article",
                    "date": "2020-01-01"
                }, {...}
            ],
            "pubmed": [
                {
                    "title": "title of article",
                    "date": "2020-01-01"
                }, {...}
            ],
            "journals": [
                {
                    "date": "2020-01-01",
                    "journal": "journal name"
                }, {...}
            ]
        },
        {...}
    ]


## Usage

### Requirements

- Python >= 3.6

#### Installation

    virtualenv -p python3 venv
    source venv/bin/activate
    
    pip install bazema_linker

Display usage
    
    bazema_linker -h
    
#### Example

    bazema_linker --input_dir data --output_dir result
    
#### Development
    
    # Install
    virtualenv -p python3 venv
    source venv/bin/activate
    make install
    
    # Build
    make test # coverage tests
    make linter # runs pylint
    make build
    
## Ad-hoc Top journals

You can get the name of the journal with the most different drugs using
the script `top_journals.py` and a result file produced by `bazema_linker`.

### Usage
    # no depedency required
    python top_journals.py result/result_2020-10-06.json
    
    # output
    Journal with most different drugs is "Science" with a total of "15" different drugs.

## TODO

 - Handle high volume of data, like few tera-octets -> use a highly scalable
  framework (i.e. Apache Spark, Apache Beam). Pay attention when broadcasting data across
  workers. 
 - Deploy to Pypi using Github Actions
