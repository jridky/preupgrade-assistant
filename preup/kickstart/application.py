# -*- coding: utf-8 -*-

"""
Class creates a kickstart for migration scenario
"""

import base64
import shutil
import os
import imp
import six

from pykickstart.constants import KS_MISSING_IGNORE, KS_SCRIPT_POST
from pykickstart.parser import KickstartParser, KickstartError, Script
from pykickstart.version import makeVersion

from preup.logger import logger, logging, LoggerHelper, logger_debug, log_message
from preup.utils import FileHelper, ProcessHelper
from preup import settings


class BaseKickstart(object):
    """ Base class used for testing tool run on final pkgs. """

    def run_module(self, *arg, **kwargs):
        """Perform the check itself and return results."""
        raise NotImplementedError()


class KickstartGenerator(object):
    """Generate kickstart using data from provided result"""

    def __init__(self, conf, dir_name, kick_start_name):
        self.dir_name = dir_name
        self.ks = None
        self.kick_start_name = kick_start_name
        self.ks_list = []
        self.repos = None
        self.latest_tarball = ""
        self.temp_file = '/tmp/part-include'
        self.conf = conf
        self.groups = []
        self.packages = []
        self.part_layout = None
        self._injector_type = 'BaseKickstart'
        self.plugin_classes = {}
        self._add_debug_log_file()

    def _add_debug_log_file(self):
        """
        Add the special report log file
        :return:
        """
        try:
            LoggerHelper.add_file_handler(logger_debug,
                                          settings.preupg_log,
                                          formatter=logging.Formatter("%(asctime)s %(levelname)s\t%(filename)s"
                                                            ":%(lineno)s %(funcName)s: %(message)s"),
                                          level=logging.DEBUG)
        except (IOError, OSError):
            logger.warning("Can not create debug log '%s'", settings.preupg_log)
        else:
            self.debug_log_file = settings.preupg_log

    def checker_find_injector(self, module):
        injectors = []
        for n in dir(module):
            attr = getattr(module, n)
            if hasattr(attr, '__base__') and attr.__base__.__name__ == self._injector_type:
                injectors.append(attr)
        return injectors

    def load_plugins(self, dir_name):
        plugin_checkers = {}
        plugins_dir = os.path.join(dir_name, 'plugins')
        for plugin in os.listdir(plugins_dir):
            if not plugin.endswith('.py'):
                continue
            modname, suffix = plugin.rsplit('.', 1)
            if suffix == 'py':
                fullpath = os.path.abspath(plugins_dir)
                f, filename, description = imp.find_module(modname, [fullpath])
                m = imp.load_module(modname, open(filename, 'U'), filename, description)
                try:
                    injs = self.checker_find_injector(m)
                    for i in injs:
                        obj = i(self.ks.handler)
                        plugin_checkers[modname] = obj
                except AttributeError as ae:
                    print (ae)
                    print ("Module '%s' does not implement `register(context)`" % modname)
        return plugin_checkers

    def get_supported_modules(self):
        """Return list of supported tools"""
        return self.plugin_classes.keys()

    def collect_data(self):
        self._remove_obsolete_data()
        collected_data = True
        self.ks = KickstartGenerator.load_or_default(KickstartGenerator.get_kickstart_path(self.dir_name),
                                                     os.path.join(self.dir_name,
                                                                  settings.KS_TEMPLATE))
        if self.ks is None:
            collected_data = False
        self.latest_tarball = self.get_latest_tarball()
        return collected_data

    def _remove_obsolete_data(self):
        if os.path.exists(KickstartGenerator.get_kickstart_path(self.dir_name)):
            lines = FileHelper.get_file_content(KickstartGenerator.get_kickstart_path(self.dir_name), "r", method=True)
            lines = [x for x in lines if not x.startswith('key')]
            FileHelper.write_to_file(KickstartGenerator.get_kickstart_path(self.dir_name), "w", lines)

    @staticmethod
    def get_kickstart_path(dir_name):
        return os.path.join(dir_name, 'anaconda-ks.cfg')

    @staticmethod
    def load_or_default(system_ks_path, ks_template):
        """ load system ks or default ks """
        ksparser = KickstartParser(makeVersion())
        try:
            ksparser.readKickstart(system_ks_path)
        except (KickstartError, IOError):
            log_message("Can't read system kickstart at %s" % system_ks_path)
            try:
                ksparser.readKickstart(ks_template)
            except AttributeError:
                log_message("There is no KS_TEMPLATE_POSTSCRIPT specified in settings.py", level=logging.DEBUG)
            except IOError:
                log_message("Can't read kickstart template %s" % settings.KS_TEMPLATE)
                return None
        return ksparser

    def delete_obsolete_issues(self):
        """ Remove obsolete items which does not exist on RHEL-7 anymore"""
        self.ks.handler.bootloader.location = None

    def embed_script(self, tarball):
        if tarball is None:
            return
        tarball_content = None
        if os.path.exists(tarball):
            tarball_content = FileHelper.get_file_content(tarball, 'rb', decode_flag=False)
            tarball_name = os.path.splitext(os.path.splitext(os.path.basename(tarball))[0])[0]
        script_str = ''
        try:
            script_path = settings.KS_TEMPLATE_POSTSCRIPT
        except AttributeError:
            log_message('KS_TEMPLATE_POSTSCRIPT is not defined in settings.py')
            return
        script_str = FileHelper.get_file_content(os.path.join(settings.KS_DIR, script_path), 'rb')
        if not script_str:
            log_message("Can't open script template: {0}".format(script_path))
            return
        if tarball_content is not None:
            script_str = script_str.replace('{tar_ball}', base64.b64encode(tarball_content))
            script_str = script_str.replace('{RESULT_NAME}', tarball_name)
            script_str = script_str.replace('{TEMPORARY_PREUPG_DIR}', '/root/preupgrade')
            script = Script(script_str, type=KS_SCRIPT_POST, inChroot=True)
            self.ks.handler.scripts.append(script)

    def save_kickstart(self):
        kickstart_data = self.ks.handler.__str__()
        FileHelper.write_to_file(self.kick_start_name, 'wb', kickstart_data)

    def update_kickstart(self, text, cnt):
        self.ks_list.insert(cnt, text)
        return cnt + 1

    @staticmethod
    def copy_kickstart_templates():
        # Copy kickstart files (/usr/share/preupgrade/kickstart) for kickstart generation
        for file_name in settings.KS_TEMPLATES:
            target_name = os.path.join(settings.KS_DIR, file_name)
            source_name = os.path.join(settings.source_dir, 'kickstart', file_name)
            if not os.path.exists(target_name) and os.path.exists(source_name):
                try:
                    shutil.copy(source_name, target_name)
                except IOError:
                    pass

    def get_prefix(self):
        return settings.tarball_prefix + settings.tarball_base

    def get_latest_tarball(self):
        tarball = None
        for directories, dummy_subdir, filenames in os.walk(settings.tarball_result_dir):
            preupg_files = [x for x in sorted(filenames) if x.startswith(self.get_prefix())]
            # We need a last file
            tarball = os.path.join(directories, preupg_files[-1])
        return tarball

    def comment_kickstart_issues(self):
        list_issues = [' --', 'group', 'user ', 'repo', 'url', 'rootpw']
        kickstart_data = []
        try:
            kickstart_data = FileHelper.get_file_content(os.path.join(settings.KS_DIR, self.kick_start_name),
                                                         'rb',
                                                         method=True,
                                                         decode_flag=False)
        except IOError:
            log_message("File %s is missing. Partitioning layout has not to be complete." % self.kick_start_name,
                        level=logging.WARNING)
            return None
        for index, row in enumerate(kickstart_data):
            tag = [com for com in list_issues if row.startswith(com)]
            if tag:
                kickstart_data[index] = "#" + row
        FileHelper.write_to_file(self.kick_start_name, 'wb', kickstart_data)

    def generate(self):
        if not self.collect_data():
            log_message("Important data are missing for kickstart generation.", level=logging.ERROR)
            return None
        self.ks.handler.packages.excludedList = []
        self.plugin_classes = self.load_plugins(os.path.dirname(__file__))
        for module in six.iterkeys(self.plugin_classes):
            self.plugin_classes[module].run_module()
        self.ks.handler.packages.handleMissing = KS_MISSING_IGNORE
        self.ks.handler.keyboard.keyboard = 'us'
        self.embed_script(self.latest_tarball)
        self.delete_obsolete_issues()
        self.save_kickstart()
        self.comment_kickstart_issues()
        return True

    def main(self):
        if not os.path.exists(os.path.join(settings.result_dir, settings.xml_result_name)):
            log_message("'preupg' command was not run yet. Run them before kickstart generation.")
            return 1

        KickstartGenerator.copy_kickstart_templates()
        dummy_ks = self.generate()
        if dummy_ks:

            tar_ball_dir = os.path.basename(self.latest_tarball).split('.')[0]
            kickstart_dir = os.path.join(os.path.dirname(self.dir_name),
                                         tar_ball_dir)
            log_message(settings.kickstart_text % (settings.PREUPGRADE_KS,
                                                   kickstart_dir,
                                                   kickstart_dir))
        KickstartGenerator.kickstart_scripts()

    @staticmethod
    def kickstart_scripts():
        try:
            lines = FileHelper.get_file_content(os.path.join(settings.common_dir,
                                                             settings.KS_SCRIPTS),
                                                "rb",
                                                method=True)
            for line in lines:
                line = line.strip()
                if line.startswith("#"):
                    continue
                if 'is not installed' in line:
                    continue
                cmd, name = line.split("=", 2)
                kickstart_file = os.path.join(settings.KS_DIR, name)
                ProcessHelper.run_subprocess(cmd, output=kickstart_file, shell=True)
        except IOError:
            pass


def run():
    KickstartGenerator()
    return
