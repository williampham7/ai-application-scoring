import torch

print(torch.__version__)
print(torch.cuda.is_available())  # Should print True
print(torch.cuda.get_device_name(0))  # Should print "RTX 4060"