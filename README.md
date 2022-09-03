# About The Project


We need system to calculate similarity between two house floor plans.

Here’s why:

- Making House!Finder;House Floor plan Recommendation System
- Calculate GED needs to long time. Because of it’s NP-Complete complexity.




# Getting Started


This is an example of how you may give instructions on setting up your project locally. To get a local copy up and running follow these simple example steps.




## ****Prerequisites****

- **python**==3.8
- **pytorch** (본인 CUDA version에 맞게)
    
    [PyTorch](https://pytorch.org/get-started/locally/)
    
- **pytorch geometric**( 본인 pytorch version과 CUDA version에 맞게)
    
    [Installation - pytorch_geometric documentation](https://pytorch-geometric.readthedocs.io/en/latest/notes/installation.html)
    
- **numpy**
- **pandas**
- **networkx**
- **argparse**
- **sklearn**
- etc) 제가 빼먹었을 수도 있는데,, 혹시나 실행했는데 ‘무슨 package?가 없습니다’ 라 뜨면 해당 package install 하면 해결될 것 입니다..!

## Execution

```python
main.bat
#if mac?
#bash main.sh
```

# If Mac?

You need to change **batch file** to  **bash file**.

### main.sh

```bash
#!/bin/bash
python ./src/main.py
```
