#!/bin/bash

echo "Loading modules..."
module load python3/3.8.10
module load opencv/4.5.0
module load cuda/11.3
module load pytorch/1.11.0
echo "Modules loaded."
pip3 install -r requirements.txt
echo "Setup complete!"