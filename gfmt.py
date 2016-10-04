#!/usr/bin/env
"""
Presentation script for the Glasgow Face Matching Test, long version.

Burton, A. M., White, D., & McNeill, A. (2010). The Glasgow Face Matching Test.
Behavior Research Methods. http://doi.org/10.3758/BRM.42.1.286
"""

from glob import glob
from os import makedirs
from os.path import join as pjoin, exists as pexists
from psychopy import visual, core, logging, data, event
import json


version = '0.0.1'


# Get subject information
def ask_subjinfo():
    from psychopy import gui
    info = {'subject_id': '',
            'subject_age': '',
            'subject_gender': ['male', 'female', 'other'],
            'version': ['long', 'short'],
            }
    info_dlg = gui.DlgFromDict(dictionary=info,
                               title='Glasgow Face Matching Test',
                               order=['subject_id',
                                      'subject_age',
                                      'subject_gender',
                                      'version'])
    if not info_dlg.OK:
        core.quit()
    return info


class GFMT(object):
    def __init__(self, info, cfgfile):
        self.stimuli = {}
        self.info = info
        self.cfg = self.load_cfg(cfgfile)
        self.experiment_handler = None
        self.trial_order = None
        self.win = None
        self.text_info = None

        self.setup_datasaver()
        self.setup_trialorder()
        self.setup_win()
        self.load_stimuli()

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
        fn_out = pjoin(subject_out_path,
                       'results_{0}'.format(self.info['version']))
        self.experiment_handler = \
            data.ExperimentHandler(name='GFMT', version=version,
                                   extraInfo=self.info,
                                   dataFileName=fn_out)

    def setup_trialorder(self):
        # make trial_list to pass to trialhandler
        trial_list = []
        for stim_type in self.cfg['stim_type']:
            for fn in glob(pjoin(self.cfg['stim_dir'],
                                 self.info['version'], stim_type)):
                trial_list.append({'stim_name': fn,
                                   'stim_type': stim_type})
        self.trial_order = data.TrialHandler(trial_list, 1, method='random')
        # add to experiment_handler
        self.experiment_handler.addLoop(self.trial_order)

    def load_stimuli(self):
        # self.stimuli is a hash table with fn -> stim obj
        for stim_type in self.cfg['stim_type']:
            for fn in glob(pjoin(self.cfg['stim_dir'],
                                 self.info['version'],
                                 stim_type)):
                self.stimuli[fn] = visual.ImageStim(self.win, image=fn)

        # save text to display under stimuli
        keys = sorted(self.cfg['response_keys'].keys())
        text = '{0}: {1}\t\t\t{2}: {3}'.format(
            keys[0],
            self.cfg['response_keys'][keys[0]],
            keys[1],
            self.cfg['response_keys'][keys[1]]
            )
        self.text_info = visual.TextStim(self.win,
                                         text,
                                         pos=(-0.5, -0.5))

    def run(self):
        for trial in self.trial_order:
            stim_name = trial['stim_name']
            # draw stimulus
            self.stimuli[stim_name].draw()
            # draw text
            self.text_info.draw()
            self.win.flip()
            # wait for response
            keys = []
            while self.cfg['response_keys'].values() not in keys:
                keys = event.getKeys()
            self.win.flip()
            # store response
            self.trial_order.addData('response',
                                     '+'.join([self.cfg['response_keys'][k]
                                               for k in keys]))
            # update to next entry in experiment handler
            self.experiment_handler.nextEntry()


def main():
    info = ask_subjinfo()
    gfmt = GFMT(info, 'pathtocfg.json')
    gfmt.run()

if __name__ == '__main__':
    main()
