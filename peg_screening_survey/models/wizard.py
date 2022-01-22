from odoo import models, fields, api
import logging
import uuid

from odoo.tools import pycompat
_logger = logging.getLogger(__name__)

class SurveyAssignContact(models.TransientModel):
    _name = 'survey.assign_contact'
    _description = 'Survey assignment wizard'

    def default_survey_id(self):
        context = self.env.context
        if context.get('model') == 'survey.survey':
            return context.get('res_id')

    def default_partner_id(self):
        context = self.env.context
        if context.get('active_model') == 'res.partner':
            return context.get('active_id')

    manual = fields.Boolean(default=True)
    survey_id = fields.Many2one('survey.survey', string='Survey', default=default_survey_id, required=True)
    partner_id = fields.Many2one(string='Customer', comodel_name='res.partner', default=default_partner_id, required=True)

    #@api.multi
    def assign_action(self):
        self.ensure_one()
        SurveyUserInput = self.env['survey.user_input']
        token = pycompat.text_type(uuid.uuid4())
        # create response with token
        SurveyUserInput.create({
            'survey_id': self.survey_id.id,
            'date_create': fields.Datetime.now(),
            'type': 'link',
            'state': 'new',
            'token': token,
            'partner_id': self.partner_id.id
            })
        _logger.debug(token)
        trail = "/%s" % token if token else ""
        
        return {
            'type': 'ir.actions.act_url',
            'name': "Start Survey",
            'target': '_blank',
            'url': self.survey_id.with_context(relative_url=True).public_url + trail
        }