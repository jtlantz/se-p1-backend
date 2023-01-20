#Django Web Application for managing vending machines for Software Engineering Class

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

#API Reference

##Viewing

###Homepage URL, displays all Vending Machines
```http
/api/
```

###View specific Vending Machine
```html
/api/vendingMachine/view/<int:vending_id>
```
| Parameter | Type  | Description                           |
|:----------|:------|:--------------------------------------|
| `id`      | `int` | **Required**. Id of a vending machine |

###View all products
```html
/api/product/view/
```

###View specific product
```html
/api/product/view/<int:product_id>
```

| Parameter | Type  | Description                           |
|:----------|:------|:--------------------------------------|
| `id`      | `int` | **Required**. Id of the product       |


###View all Stock
```html
/api/stock/view/
```

###View specific stock item
```html
/api/stock/view/<int:stock_id>
```

| Parameter | Type  | Description                           |
|:----------|:------|:--------------------------------------|
| `id`      | `int` | **Required**. Id of a vending machine |


##Creation

###Get the page to add a new machine, not necessary if using API only
```html
GET /api/vendingMachine/add/
```

###Get the page to add a new product, not necessary if using API only
```html
GET /api/product/add/
```

###Get the page to add a new stock, not necessary if using API only
```html
GET /api/stock/add/
```

###Add the vending machine
```html
POST /api/vendingMachine/add/
```
| Parameter | Type  | Description                               |
|:----------|:------|:------------------------------------------|
| 'building'| `str` | **Required**. Building for machine        |
| 'floor'   | `int` | **Required**. Floor for machine           |
| 'location'| `str` | **Required**. Classroom or area of machine|

###Add the new product
```html
POST /api/product/add/
```
| Parameter | Type  | Description                               |
|:----------|:------|:------------------------------------------|
| 'name'    | `str` | **Required**. Name of product             |
| 'price'   |`float`| **Required**. The price of the product    |
| 'on_hand' | `int` | **Required**. Amount of stock on hand     |

###Add new stock
```html
POST /api/stock/add/
```

| Parameter | Type  | Description                               |
|:-----------------|:------|:-------------------------------------------|
| 'vending_machine'| `int` | **Required**. ID of machine stock is in    |
| 'product'        | `int` | **Required**. ID of product stock points to|
| 'quantity'       | `int` | **Required**. Amount of product in machine |



##Updating

###Get the page to update the vending machine
```html
GET /api/vendingMachine/update/<int:vending_id>
```

###Get the page to update the product
```html
GET /api/product/update/<int:product_id>
```

###Get the page to update the stock
```html
GET /api/stock/update/<int:stock_id>
```


###Edit the Vending machine
```html
POST /api/vendingMachine/update/<int:vending_id>
```
| Parameter | Type  | Description                               |
|:----------|:------|:------------------------------------------|
| 'building'| `str` | **Required**. Building for machine        |
| 'floor'   | `int` | **Required**. Floor for machine           |
| 'location'| `str` | **Required**. Classroom or area of machine|


###Edit the Product
```html
POST /api/product/update/<int:product_id>
```
| Parameter | Type  | Description                               |
|:----------|:------|:------------------------------------------|
| 'price'   |`float`| **Required**. The price of the product    |
| 'on_hand' | `int` | **Required**. Amount of stock on hand     |


###Edit the stock
```html
POST /api/stock/update/<int:stock_id>
```
| Parameter | Type  | Description                               |
|:-----------------|:------|:-------------------------------------------|
| 'quantity'       | `int` | **Required**. Amount of product in machine |



##Deleting

***these will be changed to DELETE request later***

###Delete Vending machine
```html
POST /api/vendingMachine/delete/<int:vending_id>
```
| Parameter | Type  | Description                           |
|:----------|:------|:--------------------------------------|
| 'id'      | `int` | **Required**. ID of machine to delete |


###Delete product
```html
POST /api/product/delete/<int:product_id>
```
| Parameter | Type  | Description                            |
|:----------|:------|:---------------------------------------|
| 'id'      | `int` | **Required**. ID of product to delete  |


###Delete stock
```html
POST /api/stock/delete/<int:stock_id>
```
| Parameter | Type  | Description                         |
|:----------|:------|:------------------------------------|
| 'id'      | `int` | **Required**. ID of stock to delete |

