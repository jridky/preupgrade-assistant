from __future__ import unicode_literals
import sys
import os


if os.path.basename(sys.argv[0]) == "premigrate":
    prefix = "premigrate"
else:
    prefix = "preupgrade"

defenc = "utf-8" if sys.getdefaultencoding() == "ascii" else sys.getdefaultencoding()

# dir where results of analysis are stored
result_dir = os.path.join("/root", prefix)

# Dir where tar balls are placed
tarball_result_dir = result_dir+"-results"

# base name of XML and HTML file with results
result_name = "result"

tarball_base = result_name + 's'
tarball_prefix = "preupg_"
tarball_name = tarball_prefix + tarball_base + "-{0}"

xml_result_name = result_name + '.xml'
html_result_name = result_name + '.html'

# base name of custom xsl stylesheet
xsl_sheet = "xccdf-report.xsl"

old_xsl_sheet = "preup.xsl"

share_dir = "/usr/share"
# sources delivered by preupgrade assistant package
source_dir = os.path.join(share_dir, prefix)

# dir where the cached logs are stored
cache_dir = "/var/cache/preupgrade"

# file where the lock file stored
lock_file = "/var/run/preupgrade.pid"

# dir with log files"
log_dir = "/var/log/preupgrade"

# preupg log file
preupg_log = os.path.join(log_dir, "preupg.log")

# preupg report log file
preupg_report_log = os.path.join(log_dir, "preupg-report.log")

# dir where the postupgrade scripts are placed
postupgrade_dir = "postupgrade.d"

# dir with preupgrade-scripts which are executed before reboot and upgrade.
preupgrade_name = "preupgrade-scripts"
preupgrade_scripts = os.path.join(result_dir, preupgrade_name)

# dirtyconfig directory used by preupgrade assistant
dirty_conf_dir = 'dirtyconf'

# cleanconfig directory used by preupgrade assistant
clean_conf_dir = 'cleanconf'

# cleanconf directory used by preupgrade assistant
# xccdf profile
profile = "xccdf_preupg_profile_default"

# name of dir with common files
common_name = "common"

# default directory is /var/tmp/preupgrade/common
# absolute path to dir with common files
common_dir = os.path.join(share_dir, prefix, common_name)

# path to file with definitions of common scripts
common_script = os.path.join(common_dir, "scripts.txt")

# Addons dir for 3rdparty contents
add_ons = "3rdparty"

# Default content file
content_file = "all-xccdf.xml"

# prefix of tag in fccdf files
xccdf_tag = "xccdf_preupg_rule_"

# name of the hash file
base_hashed_file = "hashed_file"

# name of the file which contains a list of rules
file_list_rules = "list_rules"

# path to file with definitions of common scripts
post_script = os.path.join(common_dir, "post_scripts.txt")

# kickstart and postupgrade.d directories
preupgrade_dirs = [dirty_conf_dir, clean_conf_dir,
                   'hooks', 'kickstart', postupgrade_dir, 'common',
                   'preupgrade-scripts', 'noauto_postupgrade.d']


PREUPG_README = 'README'
readme_files = {'README': PREUPG_README,
                'README.kickstart': os.path.join('kickstart', 'README'),
                }

# Used for autogeneration check script issues
autocomplete = True

# new state needs_inspection
needs_inspection = "needs_inspection"

# new state needs_action
needs_action = "needs_action"

openscap_binary = "/usr/bin/oscap"

# The full license text
license = u"""Preupgrade Assistant performs system upgradability assessment
and gathers information required for successful operating system upgrade.
Copyright (C) 2013 Red Hat Inc.
%s
<new_line>
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
<new_line>
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
<new_line>
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>."""

warning_text = "The Preupgrade Assistant is a diagnostics tool \n" \
               "and does not perform the actual upgrade.\n" \
               "Please ensure you have backed up your system and/or data \n" \
               "in the event of a failed upgrade that would require \n" \
               "a full re-install of the system from installation media."
migration_text = "The running system is 32bit. Migration is possible only to 64bit system.\nSee help --dst-arch option.\n"
migration_options = ['i386-x86_64', 'ppc-ppc64']
assessment_text = "Assessment of the system, running checks / SCE scripts"
result_text = "Result table with checks and their results for '{0}':"
message = "We found some potential in-place upgrade risks.\n" \
          "Read the full report file '{0}' for more details."
converter_message = "At least one of these converters ({0}) needs to be installed."
kickstart_text = "The Preupgrade Assistant generates a kickstart file in '%s'.\n" \
                 "The Kickstart file contains:\n" \
                 "- users with UID/GID which you should create on Red Hat Enterprise Linux 7 system.\n" \
                 "- the partitioning layout which was used on this system\n" \
                 "- the package set which was installed on this system.\n" \
                 "- the firewall rules which were enabled on this system.\n" \
                 "The Kickstart file is pre-generated from this system and is not to be used directly for \n" \
                 "the installation of Red Hat Enterprise Linux 7.\n" \
                 "The Kickstart file needs to be modified by the administator.\n" \
                 "These directories exist on the migration system:\n" \
                 "- %s/cleanconf - configuration files which can be used on the migrated system.\n" \
                 "- %s/dirtyconf - configuration files which need to be clarified by the administrator.\n"

options_not_allowed = "Options --mode and --select-rules are not allowed together.\n"
unknown_rules = "These rules do not exist:\n%s\n"
text_converters = {'w3m': '{0} -T text/html -dump {1} > {2}',
                   'lynx': '{0} -nonumbers -nolist -force_html -dump -nolist -width=255 {1} > {2}',
                   'elinks': '{0} --no-references -dump-width 255 --no-numbering -dump {1} > {2}',
                   }

ui_command = "preupg -u http://example.com:8099/submit/ -r {0}"
openssl_command = "openssl x509 -text -in {0} | grep -A1 1.3.6.1.4.1.2312.9.1"

UPGRADE_PATH = ""
KS_DIR = os.path.join(result_dir, 'kickstart')
KS_TEMPLATE = 'default.ks'
KS_TEMPLATE_POSTSCRIPT = 'finish.sh'
KS_TEMPLATES = [KS_TEMPLATE, KS_TEMPLATE_POSTSCRIPT]
KS_FILES = ['default_grouplist-el7', 'default-optional_grouplist-el7']
KS_SCRIPTS = "kickstart_scripts.txt"
PREUPGRADE_KS = os.path.join(KS_DIR, 'preupgrade.ks')
CPE_RHEL = 'redhat:enterprise_linux'
CPE_FEDORA = 'fedoraproject:fedora'
REPORTS = ['admin', 'user']
PREUPG_CONFIG_FILE = os.path.join('/etc', 'preupgrade-assistant.conf')

DEVEL_MODE = os.path.join(cache_dir, 'devel_mode')

# Ordered dictionary because of python 2.4.

ORDERED_LIST = ['error', 'unknown', 'fail', 'needs_action', 'needs_inspection',
                'fixed', 'informational', 'not_applicable', 'not_selected',
                'not_checked', 'pass']


class ReturnValues(object):

    SCENARIO = 20
    MODE_SELECT_RULES = 21
    RISK_CLEANUP_KICKSTART = 22
    ROOT = 23
    PREUPG_BEFORE_KICKSTART = 24
    MISSING_OPENSCAP = 25
    MISSING_TEXT_CONVERTOR = 26
    SCRIPT_TXT_MISSING = 27
    SEND_REPORT_TO_UI = 28


class ModuleValues(object):

    ERROR = 15
    UNKNOWN = 14
    FAIL = 13
    NEEDS_ACTION = 13
    NEEDS_INSPECTION = 13
    FIXED = 12
    INFORMATIONAL = 11
    NOT_ALL = 10
    PASS = 0

PREUPG_RETURN_VALUES = {'error': ModuleValues.ERROR,
                        'unknown': ModuleValues.UNKNOWN,
                        'fail': ModuleValues.FAIL,
                        'needs_action': ModuleValues.NEEDS_ACTION,
                        'needs_inspection': ModuleValues.NEEDS_INSPECTION,
                        'fixed': ModuleValues.FIXED,
                        'informational': ModuleValues.INFORMATIONAL,
                        'not_applicable': ModuleValues.NOT_ALL,
                        'not_selected': ModuleValues.NOT_ALL,
                        'not_checked': ModuleValues.NOT_ALL,
                        'pass': ModuleValues.PASS
                        }
ERROR_RETURN_VALUES = ['error', 'pass', 'informational', 'fixed',
                       'not_applicable', 'not_selected',
                       'not_checked', 'unknown']