import sys
import smtplib
import sys
import getopt
from oslo_log import log as logging
from oslo_config import cfg

CONFIG_FILE = '../etc/mail_action.conf'

class smtp_agent():
    def __init__(self, SMTP_ADDRESS, SMTP_PORT,
                 ADMIN_ACCOUNT, ADMIN_PASSWORD):
        self.SMTP_ADDRESS = SMTP_ADDRESS
        self.SMTP_PORT = SMTP_PORT
        self.ADMIN_ACCOUNT = ADMIN_ACCOUNT
        self.ADMIN_PASSWORD = ADMIN_PASSWORD

        self.server = smtplib.SMTP(self.SMTP_ADDRESS,
                                   self.SMTP_PORT)
        self.server.starttls()
        self.server.login(self.ADMIN_ACCOUNT,
                          self.ADMIN_PASSWORD)

    def action_send_mail(self, user_mail, msg):
        self.server.sendmail(self.ADMIN_ACCOUNT,
                             user_mail, msg)
        self.server.quit()


def mail(params):
    """
    @brief      { maail client moudle }
    
    @param      params['user_mail']         string: send mail address
    @param      params['message']           string: slack message
    
    @return     { description_of_the_return_value }
    """
    opt_default_group = cfg.OptGroup(name='default', title='A default informations')
    default_opts = [
        cfg.IntOpt('SMTP_PORT', default='587',
                    help=('Define SMPT PORT Number')),
        cfg.StrOpt('SMTP_ADDRESS', default='smtp.gmail.com',
                    help=('Define SMTP IP ADDRESS')),
        cfg.StrOpt('SMTP_ADMIN_ACCOUNT', default='alert@kulcloud.net',
                    help=('Define smtp alert sender mail address')),
        cfg.StrOpt('SMTP_ADMIN_PASSWORD', default='kulcloud',
                    help=('Define smtp alert sender mail password')),
        cfg.StrOpt('ADMIN_MAIL_ADDRESS', default='alert@kulcloud.net',
                    help=('Define smtp alert user mail address'))
    ]
    CONF = cfg.CONF
    CONF.register_group(opt_default_group)
    CONF.register_opts(default_opts, opt_default_group)

    user_mail = params['user_mail']
    message = params['message']

    try:
        # Regsiter Agent
        agent = smtp_agent(CONF.default.SMTP_ADDRESS,
                           CONF.default.SMTP_PORT,
                           CONF.default.SMTP_ADMIN_ACCOUNT,
                           CONF.default.SMTP_ADMIN_PASSWORD)
        msg = 'Subject: {}\n\n{}'.format('NaaCS Error Notification', message)
        agent.action_send_mail(user_mail, msg)


    except RuntimeError as e:
        LOG.error("%s SMTP Agent terminated!", e)
        return {"user_mail": user_mail, "message": "Mail Send Error"}

    return { "message": msg, "user_mail": user_mail }
