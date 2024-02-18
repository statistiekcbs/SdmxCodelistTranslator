import torch
print(f"cuda available : {torch.cuda.is_available()}")
print(f"cuda devices : {torch.cuda.device_count()}")
print(f"current coda device : {torch.cuda.current_device()}")