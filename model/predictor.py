import torch
import torch.nn as nn
import torch.nn.functional as F

class Predictor(nn.Module):
    def __init__(self, num_classes, box_feat_dim, dis_feat_dim, cls_feat_dim, rom_feat_dim, dropout):
        super(Predictor, self).__init__()
        self.box_fc = nn.Linear(box_feat_dim, 4, bias=False)
        self.dis_fc = nn.Linear(dis_feat_dim, 1, bias=False)
        self.cls_fc = nn.Sequential(
            nn.Dropout(dropout),
            nn.Linear(cls_feat_dim, num_classes, bias=False)
        )

        self.read_order_fc = nn.Linear(rom_feat_dim, 4, bias=False)
        self.sol_fc = nn.Linear(rom_feat_dim, 1, bias=False)
        self.eol_fc = nn.Linear(rom_feat_dim, 1, bias=False)

    def forward(self, box_feat, dis_feat, cls_feat, rom_feat):
        pred_box = self.box_fc(box_feat.permute(0, 2, 3, 1))
        pred_box[..., :2] = torch.sigmoid(pred_box[..., :2])
        pred_box[..., 2:] = F.relu(pred_box[..., 2:])
        grids_x, grids_y = self.get_anchor_coordinates(box_feat.shape[2], box_feat.shape[3])
        pred_box[..., 0] = (pred_box[..., 0] + grids_x) / box_feat.shape[3]
        pred_box[..., 1] = (pred_box[..., 1] + grids_y) / box_feat.shape[2]

        pred_dis = self.dis_fc(dis_feat.permute(0, 2, 3, 1))
        pred_dis = torch.sigmoid(pred_dis)

        pred_cls = self.cls_fc(cls_feat.permute(0, 2, 3, 1))
        pred_cls = F.softmax(pred_cls, -1)

        rom_feat = rom_feat.permute(0, 2, 3, 1)
        pred_read_order = self.read_order_fc(rom_feat)
        pred_read_order = F.softmax(pred_read_order, -1)
        pred_sol = self.sol_fc(rom_feat)
        pred_sol = torch.sigmoid(pred_sol)
        pred_eol = self.eol_fc(rom_feat)
        pred_eol = torch.sigmoid(pred_eol)

        pred_det_rec = torch.cat(
            (pred_box.flatten(1, 2),
             pred_dis.flatten(1, 2),
             pred_cls.flatten(1, 2)), -1
        )

        return pred_det_rec, pred_read_order, pred_sol, pred_eol

    def get_anchor_coordinates(self, nGh, nGw):
        grids_x = torch.arange(nGw)
        grids_x = grids_x.expand(nGh, -1)
        grids_y = torch.arange(nGh).unsqueeze(1)
        grids_y = grids_y.expand(-1, nGw)
        return grids_x.cuda(), grids_y.cuda()


def build_predictor(cfg):
    predictor = Predictor(
        num_classes=cfg['MODEL']['PRED']['NUM_CLASSES'],
        box_feat_dim=cfg['MODEL']['FEAT']['BOX_CHANNELS'][-1],
        dis_feat_dim=cfg['MODEL']['FEAT']['DIS_CHANNELS'][-1],
        cls_feat_dim=cfg['MODEL']['FEAT']['CLS_CHANNELS'][-1],
        rom_feat_dim=cfg['MODEL']['FEAT']['ROM_CHANNELS'][-1],
        dropout=cfg['MODEL']['PRED']['DROPOUT']
    )
    return predictor