[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=jtlantz_se-p1-backend&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=jtlantz_se-p1-backend)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=jtlantz_se-p1-backend&metric=coverage)](https://sonarcloud.io/summary/new_code?id=jtlantz_se-p1-backend)

# Contents

- [Initial Repository Setup](#initial-repository-setup)

- [Running With Docker](#running-with-docker)

- [API Reference](#api-reference)
    - [Viewing](#viewing)
    - [Creation](#creation)
    - [Updating](#updating)
    - [Deletion](#deletion)


# Initial Repository Setup

## Setup Instruction
```
poetry install
```

## Run Test
```
poetry run pytest
```

## What to do next

### Install Pre-commit (Recommended)
```
poetry run pre-commit install
```
If you wish to edit pre-commit behavior see ```.pre-commit-config.yaml```.
Normally it checks only the file you are committing. But if you wish to run it manually for all files do
```
poetry run pre-commit run --all
```

### Install Jupyter Notebook Kernel
```
poetry run python -m ipykernel install --user --name automated_clean_code
```

### Adjusting the Dependencies
edit pyproject.toml or just do
```
poetry add numpy
```
or for dev dependencies
```
poetry add --dev numpy
```
See [python-poetry.org](https://python-poetry.org/)

### Change Pytest, Flake, Coverage Setting
See ```tox.ini```

### Change how sonarqube behaves.
See ```sonar-project.properties```

### Get Pycharm to show the correct coverage
Ironically in pycharm test configuration add `--no-cov` to `Additional Arguments` this turn off pytest-cov coverage and uses Pycharm's own pytest


# Running With Docker

To run this project the user needs to have Docker and docker-compose installed

When running the project for the first time use

```bash
docker-compose up --build -d
```

When running the project all times after use
```bash
docker-compose up -d
```

***Note:*** -d is running the project in detached mode which requires running

```bash
docker-compose down
```

when ending the project. Omit running with `-d` and use `ctrl+c` to end when running in attached mode.

The following APIs are available, there is also a basic frontend framework implemented by visiting `localhost:8000/api/`

The entire project uses *Django* and it's built in frameworks. The database for this project is postgresql, startup information can be found [here](docker-compose.yaml)

# API Reference

## Viewing

### Homepage URL, displays all Vending Machines
```http
/api/
```

### View specific Vending Machine
```html
/api/machine/view/<int:vending_id>
```
| Parameter | Type  | Description                           |
|:----------|:------|:--------------------------------------|
| `id`      | `int` | **Required**. Id of a vending machine |

### View all products
```html
/api/product/view/
```

### View specific product
```html
/api/product/view/<int:product_id>
```

| Parameter | Type  | Description                           |
|:----------|:------|:--------------------------------------|
| `id`      | `int` | **Required**. Id of the product       |


### View all Stock
```html
/api/stock/view/
```

### View specific stock item
```html
/api/stock/view/<int:stock_id>
```

| Parameter | Type  | Description                           |
|:----------|:------|:--------------------------------------|
| `id`      | `int` | **Required**. Id of a vending machine |


## Creation

### Get the page to add a new machine, not necessary if using API only
```html
GET /api/machine/add/
```

### Get the page to add a new product, not necessary if using API only
```html
GET /api/product/add/
```

### Get the page to add a new stock, not necessary if using API only
```html
GET /api/stock/add/
```

### Add the vending machine
```html
POST /api/machine/add/
```
| Parameter | Type  | Description                               |
|:----------|:------|:------------------------------------------|
| 'building'| `str` | **Required**. Building for machine        |
| 'floor'   | `int` | **Required**. Floor for machine           |
| 'location'| `str` | **Required**. Classroom or area of machine|

### Add the new product
```html
POST /api/product/add/
```
| Parameter | Type  | Description                               |
|:----------|:------|:------------------------------------------|
| 'name'    | `str` | **Required**. Name of product             |
| 'price'   |`float`| **Required**. The price of the product    |
| 'on_hand' | `int` | **Required**. Amount of stock on hand     |

### Add new stock
```html
POST /api/stock/add/
```

| Parameter | Type  | Description                               |
|:-----------------|:------|:-------------------------------------------|
| 'vending_machine'| `int` | **Required**. ID of machine stock is in    |
| 'product'        | `int` | **Required**. ID of product stock points to|
| 'quantity'       | `int` | **Required**. Amount of product in machine |



## Updating

### Get the page to update the vending machine
```html
GET /api/machine/update/<int:vending_id>
```

### Get the page to update the product
```html
GET /api/product/update/<int:product_id>
```

### Get the page to update the stock
```html
GET /api/stock/update/<int:stock_id>
```


### Edit the Vending machine
```html
POST /api/machine/update/<int:vending_id>
```
| Parameter | Type  | Description                               |
|:----------|:------|:------------------------------------------|
| 'building'| `str` | **Required**. Building for machine        |
| 'floor'   | `int` | **Required**. Floor for machine           |
| 'location'| `str` | **Required**. Classroom or area of machine|


### Edit the Product
```html
POST /api/product/update/<int:product_id>
```
| Parameter | Type  | Description                               |
|:----------|:------|:------------------------------------------|
| 'price'   |`float`| **Required**. The price of the product    |
| 'on_hand' | `int` | **Required**. Amount of stock on hand     |


### Edit the stock
```html
POST /api/stock/update/<int:stock_id>
```
| Parameter | Type  | Description                               |
|:-----------------|:------|:-------------------------------------------|
| 'quantity'       | `int` | **Required**. Amount of product in machine |



## Deleting

***these will be changed to DELETE request later***

### Delete Vending machine
```html
POST /api/machine/delete/<int:vending_id>
```
| Parameter | Type  | Description                           |
|:----------|:------|:--------------------------------------|
| 'id'      | `int` | **Required**. ID of machine to delete |


### Delete product
```html
POST /api/product/delete/<int:product_id>
```
| Parameter | Type  | Description                            |
|:----------|:------|:---------------------------------------|
| 'id'      | `int` | **Required**. ID of product to delete  |


### Delete stock
```html
POST /api/stock/delete/<int:stock_id>
```
| Parameter | Type  | Description                         |
|:----------|:------|:------------------------------------|
| 'id'      | `int` | **Required**. ID of stock to delete |
