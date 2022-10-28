# PageNet: Towards End-to-End Weakly Supervised Page-Level Handwritten Chinese Text Recognition

The official implementation of [PageNet: Towards End-to-End Weakly Supervised Page-Level Handwritten Chinese Text Recognition](https://arxiv.org/abs/2207.14807) (IJCV 2022). 

## Environment
We recommend using [Anaconda](https://www.anaconda.com/) to manage environments.
```
conda create -n pagenet python=3.7 -y 
conda activate pagenet
git clone https://github.com/shannanyinxiang/PageNet
cd PageNet
pip install -r requirements.txt
```

## Dataset
- ICDAR2013 Competition Dataset: [BaiduNetDisk](https://pan.baidu.com/s/1uM2u1O9cByZtOdXyBUs6lw?pwd=uqxp) or [Google Drive](https://drive.google.com/drive/folders/120phawO79BxCSgzwaBl1vO6iYXexzZeB?usp=share_link)

Download the datasets and put them into the `datasets` folder following the file structure below.
```
datasets
└─IC13Comp
```

## Inference

### ICDAR2013 Competition Dataset 

1. Download the pretrained weights from [BaiduNetDisk](https://pan.baidu.com/s/1heCOprsoAlIIwHre-R2m1g?pwd=uf5k) or [Google Drive](https://drive.google.com/file/d/1idxOQzWeivuIkpP91E1EM3Iym4ojtRmu/view?usp=share_link) and put it into the `outputs/casia-hwdb/checkpoints` folder.

2. Run the following command:
```
python main.py --config configs/casia-hwdb.yaml
```
The results will be saved at `outputs/casia-hwdb/val_log.txt`.

## Training
Currently the training codes are not available. For questions about model training, please contact Prof. Lianwen Jin (eelwjin@scut.edu.cn) and Mr. Dezhi Peng (eedzpeng@mail.scut.edu.cn).

Note: In the spatial matching of the weakly supervised learning, we found it better to simply delete the matching pairs whose IoUs are equal to zero.

## Citation
```
@article{peng2022pagenet,
  title={PageNet: Towards End-to-End Weakly Supervised Page-Level Handwritten Chinese Text Recognition},
  author={Peng, Dezhi and Jin, Lianwen and Liu, Yuliang and Luo, Canjie and Lai, Songxuan},
  journal={International Journal of Computer Vision},
  pages={2623--2645},
  year={2022},
  volume={130},
  number={11},
  doi={10.1007/s11263-022-01654-0},
}
```

## Copyright
This repository can only be used for non-commercial research purpose.

For commercial use, please contact Prof. Lianwen Jin (eelwjin@scut.edu.cn).

Copyright 2022, [Deep Learning and Vision Computing Lab](http://www.dlvc-lab.net), South China University of Technology. 