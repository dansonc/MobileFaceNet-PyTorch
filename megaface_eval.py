import subprocess

import torch

from config import device
from megaface_utils import gen_feature, remove_noise


# from torch import nn


def megaface_test(model):
    cmd = 'find megaface/FaceScrub_aligned -name "*.bin" -type f -delete'
    print(cmd)
    output = subprocess.check_output(cmd, shell=True).decode("utf-8")
    print(output)

    cmd = 'find megaface/MegaFace_aligned/FlickrFinal2 -name "*.bin" -type f -delete'
    print(cmd)
    output = subprocess.check_output(cmd, shell=True).decode("utf-8")
    print(output)

    gen_feature('megaface/FaceScrub_aligned', model)
    gen_feature('megaface/MegaFace_aligned/FlickrFinal2', model)
    remove_noise()

    cmd = 'python megaface/devkit/experiments/run_experiment.py -p megaface/devkit/templatelists/facescrub_uncropped_features_list.json megaface/MegaFace_aligned/FlickrFinal2 megaface/FaceScrub_aligned _0.bin results -s 1000000'
    # print(cmd)
    output = subprocess.check_output(cmd, shell=True).decode("utf-8")
    # print(output)

    lines = output.split('\n')
    line = [l for l in lines if l.startswith('Rank 1: ')][0]
    accuracy = float(line[8:])

    print('Megaface accuracy: ' + str(accuracy))

    return accuracy


if __name__ == '__main__':
    checkpoint = 'BEST_checkpoint.tar'
    print('loading model: {}...'.format(checkpoint))
    checkpoint = torch.load(checkpoint)
    model = checkpoint['model'].module.to(device)
    model.eval()

    megaface_test(model)
