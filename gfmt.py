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
            'debug': False
            }
    info_dlg = gui.DlgFromDict(dictionary=info,
                               title='Glasgow Face Matching Test',
                               order=['subject_id',
                                      'subject_age',
                                      'subject_gender',
                                      'version',
                                      'debug'])
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
        debug = self.info['debug']
        if debug:
            self.win = visual.Window(size=(1024, 768), allowGUI=False,
                                     color=(1, 1, 1), screen=1, fullscr=False)
        else:
            self.win = visual.Window(allowGUI=False, color=(1, 1, 1),
                                     screen=1, fullscr=True)

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

    def get_stimtype_dir(self, stim_type):
        return pjoin(self.cfg['stim_dir'], self.info['version'], stim_type)

    def setup_trialorder(self):
        # make trial_list to pass to trialhandler
        trial_list = []
        for stim_type in self.cfg['stim_type']:
            for fn in glob(pjoin(self.get_stimtype_dir(stim_type), '*.jpg')):
                trial_list.append({'stim_name': fn,
                                   'stim_type': stim_type})
        self.trial_order = data.TrialHandler(trial_list, 1, method='random')
        # add to experiment_handler
        self.experiment_handler.addLoop(self.trial_order)

    def load_stimuli(self):
        # self.stimuli is a hash table with fn -> stim obj
        for stim_type in self.cfg['stim_type']:
            for fn in glob(pjoin(self.get_stimtype_dir(stim_type), '*.jpg')):
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
                                         pos=(0, -0.8),
                                         color=(-1, -1, -1))

    def run(self):
        # display welcome text from qualtrics version
        welcome_text = \
        "This is the face matching task. During this task you will be shown " \
        "pairs of faces. Images were taken with a variety of cameras so a " \
        "match will not be between identical images but images of the same " \
        "individual. Respond 'same' if they show the same individual." \
        "Respond 'different' if they show different individuals."  \
        "\n\nThis task is not timed. Please press any key to begin the task."

        welcome_stim = visual.TextStim(self.win,
                                       welcome_text,
                                       color=(-1, -1, -1))
        welcome_stim.draw()
        self.win.flip()
        event.waitKeys()
        self.win.flip()
        core.wait(1)

        # start experiment
        for trial in self.trial_order:
            stim_name = trial['stim_name']
            # draw stimulus
            self.stimuli[stim_name].draw()
            # draw text
            self.text_info.draw()
            self.win.flip()
            # wait for response
            response_keys = self.cfg['response_keys'].keys()
            # XXX: this assumes that only two responses are possible
            keys = []
            while response_keys[0] not in keys \
                    and response_keys[1] not in keys:
                keys = event.getKeys()
                if 'escape' in keys or 'esc' in keys:
                    self.win.close()
                    core.quit()
            self.win.flip()
            # store response
            self.trial_order.addData('response',
                                     '+'.join([self.cfg['response_keys'][k]
                                               for k in keys]))
            # update to next entry in experiment handler
            self.experiment_handler.nextEntry()
            core.wait(0.5)


def main():
    info = ask_subjinfo()
    gfmt = GFMT(info, 'config.json')
    gfmt.run()

if __name__ == '__main__':
    main()
