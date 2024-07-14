#!/bin/bash
#rm -rf ./__pychache__
export PYTHONDONTWRITEBYTECODE=1
python3 /home/jovyan/work/config_coco_core.py
python3 /home/jovyan/work/config_coco_datalake.py
python3 /home/jovyan/work/config_coco_development.py
echo "Launching Jupyter notebook server.."
#exec jupyter notebook "$@"
#python3 config_cocoMDS2.py
