# Shift Schedule Builder Dekstop``

## Environment Setup

**It is highly recommended that using the virtual environment**

### Setup virtual enviornment

```shell=
$> python3 -m venv [env name]
```

Install the required packages.

```shell=
$> python3 -m pip install -r requirements.txt
```


### Compile the `form.ui` file

```shell=
$> pyside6-uic form.ui -o ui_form.py
```

**Remember puting the `config.yaml` file into the directory**