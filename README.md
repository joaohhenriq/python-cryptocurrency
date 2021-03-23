# Cryptocurrency
Creating a cryptocurrency in a blockchain and connecting some nodes 

## Steps

> 1° - Run cryptocurrency_5001.py file

> 2° - Run cryptocurrency_5002.py file

> 3° - Run cryptocurrency_5003.py file

> 4° - In Postman create 3 tabs and put in each one, respectively: http://127.0.0.1:5001/get_chain , http://127.0.0.1:5002/get_chain , http://127.0.0.1:5003/get_chain (each of them represents a node)

> 5° - Execute each endpoint using GET Request (now all nodes have their own first block)

> 6° - Execute for each node the endpoint /conect_node as a POST Request, adding in the body the json present in nodes.json (remeber to remove the url that represents the node, ex: if you're running http://127.0.0.1:5001/get_chain, you gotta add only nodes that represent 5002 and 5003 ports)

> 7° - In the first node, run the endpoint /mine_block

> 8° - Nodes 5002 and 5003 are now out dated. Run in both the endpoint /replace_chain (it'll update them with the first node block, and guarantee that all nodes have the same blocks)

> 9° - Enjoy it the way you want

## Methods

### Gets Chain
```bash
http://127.0.0.1:5000/get_chain (GET)
```

### Mines a block
```bash
http://127.0.0.1:5000/mine_block (GET)
```

### Checks if the chain is valid
```bash
http://127.0.0.1:5000/is_valid (GET)
```

### Adds a transaction to be used in the next block you mine
```bash
http://127.0.0.1:5000/add_transaction (POST)
```

### Connects the nodes
```bash
http://127.0.0.1:5000/conect_node (POST)
```

### Updates the blockchain in a node
```bash
http://127.0.0.1:5000/replace_chain (GET)
```
