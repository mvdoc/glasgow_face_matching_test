#!/usr/bin/env
"""
Presentation script for the Glasgow Face Matching Test, long version.

Burton, A. M., White, D., & McNeill, A. (2010). The Glasgow Face Matching Test.
Behavior Research Methods. http://doi.org/10.3758/BRM.42.1.286
"""

from glob import glob
from os import makedirs
from os.path import join as pjoin, exists as pexists
from psychopy import visual, core, logging, data
import json


version = '0.0.1'


# Get subject information
def ask_subjinfo():
    from psychopy import gui
    info = {'subject_id': '',
            'subject_age': '',
            'subject_gender': ['male', 'female', 'other'],
            }
    info_dlg = gui.DlgFromDict(dictionary=info,
                               title='Glasgow Face Matching Test',
                               order=['subject_id',
                                      'subject_age',
                                      'subject_gender'])
    if not info_dlg.OK:
        core.quit()
    return info


class GFMT(object):
    def __init__(self, info, cfgfile):
        self.stimuli = []
        self.info = info
        self.cfg = self.load_cfg(cfgfile)
        self.experiment_handler = None
        self.win = None

        self.setup_datasaver()
        self.setup_win()

    @staticmethod
    def load_cfg(cfgfile):
        with open(cfgfile) as f:
            cfg = json.load(f)
        return cfg

    def setup_win(self):
        # XXX: this will get values from the cfg
        self.win = visual.Window(size=(1024, 768), allowGUI=False,
                            color=(-1, -1, -1), screen=1, fullscr=True)

    def setup_datasaver(self):
        # check output path
        out_path = self.cfg['out_path']
        subject_out_path = pjoin(out_path, self.info['subject_id'])
        if not pexists(subject_out_path):
            makedirs(subject_out_path)

        # setup experimenthandler
        self.experiment_handler = \
            data.ExperimentHandler(name='GFMT', version=version,
                                   extraInfo=self.info,
                                   dataFileName=pjoin(subject_out_path,
                                                      'results'))

    def load_stimuli(self):
        # store in self.stimuli a tuple with stimulus object and type
        for stim_type in self.cfg['stim_type']:
            for fn in glob(pjoin(self.cfg['stim_dir'], stim_type)):
                win_stim = visual.ImageStim(self.win,
                                            image=fn)
                self.stimuli.append((win_stim, stim_type))

    def trial(self, stim):
        pass

    def run(self):
        pass


def main():
    info = ask_subjinfo()
    gfmt = GFMT(info, 'pathtocfg.json')
    gfmt.run()

if __name__ == '__main__':
    main()