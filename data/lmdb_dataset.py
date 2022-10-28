import cv2
import lmdb
import numpy as np

from torch.utils.data import Dataset


class LmdbDataset(Dataset):

    def __init__(self, lmdb_dir, transforms=None):
        self.env = lmdb.open(lmdb_dir, max_readers=1, readonly=True, 
            lock=False, readahead=False, meminit=False)

        with self.env.begin(write=False) as txn:
            self.num_samples = int(txn.get('num-samples'.encode()).decode())

        self.transforms = transforms

    def __getitem__(self, idx):
        idx += 1
        image_key = f'image-{idx:06d}'.encode()
        label_key = f'label-{idx:06d}'.encode()
        num_char_key = f'numchar-{idx:06d}'.encode()
        image_shape_key = f'image-shape-{idx:06d}'.encode()
        filename_key = f'filename-{idx:06d}'.encode()
        with self.env.begin(write=False) as txn:
            image_buf = txn.get(image_key)
            label_buf = txn.get(label_key)
            num_char_buf = txn.get(num_char_key)
            image_shape_buf = txn.get(image_shape_key)
            filename = txn.get(filename_key).decode()
        
        image_shape = np.frombuffer(image_shape_buf, np.int32).tolist()
        image = np.frombuffer(image_buf, np.uint8).reshape(*image_shape).copy()
        label = np.frombuffer(label_buf, np.float32).reshape(-1, 5).copy()
        num_char_per_line = np.frombuffer(num_char_buf, np.int32).copy()
        sample = {
            'image': image,
            'label': label,
            'num_char_per_line': num_char_per_line,
            'filename': filename,
            'ori_shape': image_shape,
            'image_shape': image_shape
        }

        if self.transforms is not None:
            sample = self.transforms(sample)
        
        return sample
            
    def __len__(self):
        return self.num_samples
